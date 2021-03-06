#!/usr/bin/env python
# script to deploy codes

import os
import subprocess

import fire

PYENV_INSTALLER_URL = 'https://raw.githubusercontent.com/' + \
    'pyenv/pyenv-installer/master/bin/pyenv-installer'

PYENV_SETUP_COMMANDS = [
    'export PATH="$HOME/.pyenv/bin:$PATH"', 'eval "$(pyenv init -)"',
    'eval "$(pyenv virtualenv-init -)"'
]

def install_pyenv(hostname):
    'Install pyenv on remote host via ssh'
    print('> Installing pyenv')
    subprocess.check_call(['ssh', hostname, 'curl -L %s | bash' % PYENV_INSTALLER_URL])

def concatenate_shell_commands(commands, separator=';'):
    'Concatenate multiple shell command'
    return ''.join([c + separator for c in commands])


def install_python(hostname, version='3.5.2'):
    'Install python using pyenv on remote host'
    commands = PYENV_SETUP_COMMANDS + [
        'pyenv install %s -s' % version,
        'pyenv global %s' % version,
        'pip install -U virtualenv',
    ]
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def deploy_source_code(hostname, target_directory):
    'Copy source code to remote host'
    exclude_directories = [
        '.venv',
        '.idea',
        '.git',
        '__pycache__',
        '*.pyc',
        'node_modules',
        'bower_components',
        'ts_build',
    ]
    from_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    exclude_options = ['--exclude=%s' % d for d in exclude_directories]
    subprocess.check_call(
        ['rsync', '-avz'] + exclude_options +
        [from_directory + '/', '%s:%s/' % (hostname, target_directory)])


def build_python_code(hostname, target_directory):
    'Build python code using `python setup.py develop` on remote host'
    # install libleveldb-dev is required
    commands = PYENV_SETUP_COMMANDS + [
        'cd %s' % target_directory,
        'test -d .venv || virtualenv .venv',
        'source .venv/bin/activate',
        'python setup.py develop',
    ]
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def copy_environmental_variables(hostname, target_directory):
    envs = ['LOGGLY_TOKEN', 'CLOUDMQTT_URL', 'IFTTT_KEY']
    content = ';'.join(['export %s=%s' % (env, os.environ[env]) for env in envs])
    commands = ['cd %s' % target_directory, 'echo "%s" > setup.sh' % content]
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def setup_systemd(hostname, target_directory):
    'Prepare user-local systemd setting'
    service_file = 'tools/home-mqtt-url-relay.service'
    sed_command = 'sed -e s+@PROJECT_DIR@+${PWD}+g -i %s' % (service_file)
    commands = [
        'cd %s' % target_directory,
        sed_command,
        'mkdir -p ${HOME}/.config/systemd/user/',
        # Be careful, symbolic link of .service file does not work.
        'cp ${PWD}/%s ${HOME}/.config/systemd/user/' % service_file,
        'systemctl --user daemon-reload',
        'systemctl --user enable home-mqtt-url-relay',
        'systemctl --user restart home-mqtt-url-relay',
    ]
    print(concatenate_shell_commands(commands))
    subprocess.check_call(['ssh', hostname, concatenate_shell_commands(commands)])


def main_impl(hostname, target_directory):
    'Main function'
    print('> Start deploying to %s' % hostname)
    install_pyenv(hostname)
    install_python(hostname)
    deploy_source_code(hostname, target_directory)
    build_python_code(hostname, target_directory)
    copy_environmental_variables(hostname, target_directory)
    setup_systemd(hostname, target_directory)
    print('Please run `sudo loginctl enable-linger ${USER}` to enable auto start')


def main():
    'Entry point for command line usage'
    os.environ['LANG'] = 'C'
    os.environ['LC_ALL'] = 'C'
    fire.Fire(main_impl)


if __name__ == '__main__':
    main()
