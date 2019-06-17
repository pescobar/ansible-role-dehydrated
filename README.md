[![Build Status](https://travis-ci.org/pescobar/ansible-role-dehydrated.svg?branch=master)](https://travis-ci.org/pescobar/ansible-role-dehydrated)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-pescobar.dehydrated-blue.svg)](https://galaxy.ansible.com/pescobar/dehydrated)

ansible-role-dehydrated
=========

Install the dehydrated letsencrypt/acme client

Role Variables
--------------
```
dehydrated_config_dir: "/etc/dehydrated"

dehydrated_wellknown_dir: "/var/www/dehydrated/"

dehydrated_certs_dir: "{{ dehydrated_config_dir }}/certs"

dehydrated_version: "master"

dehydrated_install_dir: "/usr/local/bin"

dehydrated_contact_email: "dummy@dummy.com"

dehydrated_domains:
  - "{{ ansible_fqdn }}"
```

License
-------

GPLv3

Author Information
------------------

Pablo Escobar
