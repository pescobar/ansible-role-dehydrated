import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_dehydrated_config(host):
    f = host.file('/etc/dehydrated/config')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert oct(f.mode) == '0o644'
    assert f.contains('CONTACT_EMAIL')


def test_dehydrated_domains_file(host):
    f = host.file('/etc/dehydrated/domains.txt')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert oct(f.mode) == '0o644'


def test_dehydrated_script(host):
    f = host.file('/usr/local/bin/dehydrated')
    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert oct(f.mode) == '0o755'
