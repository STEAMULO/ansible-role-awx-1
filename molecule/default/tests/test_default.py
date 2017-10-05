import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_containers_running(host):
    ps = host.check_output('docker ps')
    assert 'awx_web' in ps
    assert 'awx_task' in ps
    assert 'rabbitmq' in ps
    assert 'postgres' in ps
    assert 'memcached' in ps


def test_awx_listening(host):
    assert host.socket('tcp://0.0.0.0:80').is_listening


def test_secret_key(host):
    assert host.file('/etc/awx_secret_key').is_file
