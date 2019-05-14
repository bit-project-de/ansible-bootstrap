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
sudo apt install python-pip
sudo pip install virtualenv
```

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
