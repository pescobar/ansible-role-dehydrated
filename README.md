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

dehydrated_hook_script_path: "{{ dehydrated_config_dir }}/hook.sh"

# this is the command executed when a new cert is deployed
# this command is defined in the function deploy_cert() in
# the dehydrated hook script
dehydrated_hook_deploy_cert_cmd: |
  systemctl reload httpd
```

Example playbook (using [geerlingguy.apache](https://galaxy.ansible.com/geerlingguy/apache))
---------------
```
- name: Configure webserver with ssl
  hosts: webserver
  gather_facts: True
  remote_user: root

  vars:

    dehydrated_contact_email: "myemail@foo.com"

    vhost_public_domain: mycoolweb.com

    apache_global_vhost_settings: |
      DirectoryIndex index.php index.html
      Alias /.well-known/acme-challenge/ {{ dehydrated_wellknown_dir }}
      <Directory {{ dehydrated_wellknown_dir }} >
          Require all granted
      </Directory>

    apache_vhosts:
      - servername: "{{ vhost_public_domain }}"
        serveralias: "www.{{ vhost_public_domain }}"
        serveradmin: "{{ dehydrated_contact_email }}"
        documentroot: "/var/www/{{ vhost_public_domain }}"
        extra_parameters: |

          # redirect all traffic to https except the letsencrypt requests
          RewriteEngine On
          RewriteCond %{HTTPS} off
	  RewriteCond %{REQUEST_URI} !^/.well-known/
          RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [R,L]

    apache_vhosts_ssl:
      - servername: "{{ vhost_public_domain }}"
        serveralias: "www.{{ vhost_public_domain }}"
        serveradmin: "{{ dehydrated_contact_email }}"
        documentroot: "/var/www/{{ vhost_public_domain }}"
        certificate_file: "{{ dehydrated_certs_dir }}/{{ vhost_public_domain }}/cert.pem"
        certificate_key_file: "{{ dehydrated_certs_dir }}/{{ vhost_public_domain }}/privkey.pem"
        certificate_chain_file: "{{ dehydrated_certs_dir }}/{{ vhost_public_domain }}/fullchain.pem"

    # this var is required by role "geerlingguy.apache" so ssl vhosts
    # are only configured when the ssl certificate exists.
    apache_ignore_missing_ssl_certificate: false

  tasks:

    - name: Install and configure apache webserver (no ssl yet)
      import_role:
        name: geerlingguy.apache

    - name: Install dehydrated letsencrypt/acme client
      import_role:
        name: ansible-role-dehydrated

    # execute handlers so apache enables the .well-known folder and
    # dehydrated requests the ssl certificates
    - meta: flush_handlers

    - name: Install and configure apache webserver again (configure ssl vhosts)
      import_role:
        name: geerlingguy.apache
```

License
-------

GPLv3

Author Information
------------------

Pablo Escobar
