# Testing

This role uses [tox](https://tox.readthedocs.io), [molecule](https://molecule.readthedocs.io)
and [LXD](https://linuxcontainers.org/lxd/) to test different scenarios and environments.

## Prerequisites (on Ubuntu)

Prepare lxd based on snap:
```
snap install lxd
lxd init
```
Prepare global python requirements:
```
sudo apt install python-pip curl
sudo pip install virtualenv
```

Prepare pyenv to install missing python versions (optional):
```
curl https://pyenv.run | bash
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
```
*Restart terminal session or execute `exec "$SHELL"` afterwards.*

## Prepare Environment
```
virtualenv --no-site-packages .venv
source .venv/bin/activate
pip install -r test-requirements.txt
```

## Tox Usage

Run all tests:
```
tox
```

List available environments:
```
tox -l
```

Run tests in specific environment:
```
tox -e py27-ansible27
```

Run custom command in specific environment:
```
tox -e py27-ansible27 -- molecule converge
```

## ARA Usage

For better debugging tox is configured to run with an [ARA](https://ara.readthedocs.io/)
enabled environment. While running the Ansible callback plugin for ARA records all
playbook runs into a local sqlite database `.ara/ansible.sqlite`.

After running the tests you can visualize the plays running the ARA webserver:
```
tox -e  py27-ansible27 -- ara-manage runserver
```
