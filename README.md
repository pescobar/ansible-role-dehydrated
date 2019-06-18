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

Example playbook (using [geerlingguy.apache](https://galaxy.ansible.com/geerlingguy/apache))
---------------
```
- name: Configure webserver with ssl
  hosts: webserver
  gather_facts: True
  remote_user: root

  vars:

    # this var is required by role "geerlingguy.apache" so ssl vhosts 
    # are only configured when the ssl certificate exists.
    apache_ignore_missing_ssl_certificate: false

    apache_global_vhost_settings: |
      DirectoryIndex index.php index.html
      Alias /.well-known/acme-challenge/ {{ dehydrated_wellknown_dir }}
      <Directory {{ dehydrated_wellknown_dir }} >
          Require all granted
      </Directory>

    dehydrated_contact_email: "myemail@foo.com"

  tasks:

    - name: Configure apache webserver (no ssl yet)
      import_role:
        name: geerlingguy.apache

    - name: Install dehydrated
      import_role:
        name: ansible-role-dehydrated

    # execute dehydrated handlers so the ssl certs are downloaded
    - meta: flush_handlers

    - name: Install apache webserver (configure ssl vhosts)
      import_role:
        name: geerlingguy.apache
```

License
-------

GPLv3

Author Information
------------------

Pablo Escobar
