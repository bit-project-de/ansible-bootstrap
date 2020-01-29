import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_python(host):
    python_version = host.run("python -V")
    if python_version.rc != 0:
        python_version = host.run("python2 -V")
        if python_version.rc != 0:
            python_version = host.run("python3 -V")

    assert python_version.rc == 0
