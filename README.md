## Introduction

Checkpoints:

- install Odoo 17 on-premise with Source install on Ubuntu Server 24.04.1 LTS
- Odoo 17 tutorials: Server framework 101
- Add AEODOO training of Odoo 17


## Tutorial - Server framework 101

- [Setup guide](md/0_setup.md)
- [Chapter 1: Architecture Overview](md/01_architecture_overview.md)
- [Chapter 2: A New Application](md/02_a_new_application.md)
- [Chapter 3: Models And Basic Fields](md/03_models_and_basic_fields.md)
- [Chapter 4: Security - A Brief Introduction](md/04_security_a_brief_introduction.md)
- [Chapter 5: Finally, Some UI To Play With](md/05_finally_some_ui_to_play_with.md)
- [Chapter 6: Basic Views](md/06_basic_views.md)
- [Chapter 7: Relations Between Models](md/07_relations_between_models.md)
- [Chapter 8: Computed Fields And Onchanges](md/08__computed_fields_and_onchanges.md)
- [Chapter 9: Ready For Some Action?](md/09_ready_for_some_action.md)
- [Chapter 10: Constraints](md/10_constraints.md)
- [Chapter 11: Add The Sprinkles](md/11_add_the_sprinklesy.md)
- [Chapter 12: Inheritance](md/12_inheritance.md)



## Run
- `cd odoo17`
- `source venv/bin/activate` 
- or `. venv/bin/activate`
- `python3 odoo-bin -c odoo.conf` 
- or `./odoo-bin -c odoo.conf`
- http://192.168.1.60:8069/


## Run Tutorials
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate`
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate --dev xml`
- or `./odoo-bin -c odoo.conf` if configure params in **odoo.conf**

- **odoo.conf**
```
[options]
; This is the password that allows database operations:
; admin_passwd = admin
db_host = False
db_port = False
db_user = aleon
;db_password = 
db_name = rd-demo
addons_path = addons/, custom/, tutorials/, cursaeodoo/
default_productivity_apps = True
```


## Run with Debug
- run `source .bin/debug.sh`
- to fix connections on port
```
lsof -i :5678
sudo kill -9 <process_id>
```

## AEODOO Training
- active `veterinary_clinic` and `veterinary_clinic_sale` modules
- add Veterinary Clinic `Manager` group in current admin user
- (Settings / Users / User / Other / Veterinary Clinic)



## Requeriments / Prerequisites

```
OS: Ubuntu noble 24.04 x86_64
Host: VMware Virtual Platform
Kernel: Linux 6.8.0-41-generic
```

- 🖥️ `lsb_release -a`
```
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 24.04.1 LTS
Release:        24.04
Codename:       noble
```

- 🖥️ `git --version`
```
git version 2.43.0
```

- 🖥️ `python3 --version`
```
Python 3.12.3
```

- 🖥️ `pip3 --version`
```
pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)
```

- 🖥️ `sudo -u postgres psql`
```
psql (16.4 (Ubuntu 16.4-0ubuntu0.24.04.2))
```




## Dependencies

- python3-pip
- python3-venv
- wkhtmltopdf (HTML to PDF)
- others




## Dev environment

### host
- Microsoft Windows [Versión 10.0.19045.4780]
- Visual Studio Code 1.93.0
- Visual Studio Extension > `Remote Explorer` for SSH
- VMware® Workstation 17 Player [17.5.2 build-23775571]
- DBeaver [Version 24.2.0.202409011551]

### virtual host
- Ubuntu Server 24.04.1 LTS




## Project Steps

### Ubuntu Server
- download ISO in https://ubuntu.com/download/server
- create new virtual machine in VMware Player and booth with Ubuntu ISO
- install Ubuntu Server with *SSH* service

### Netplan
- configure *Netplan* in `/etc/netplan`
- `sudo cat /etc/netplan/50-cloud-init.yaml`
```
network:
    version: 2
    renderer: networkd
    ethernets:
        ens33:
            dhcp4: no
            addresses:
              - 192.168.1.60/24
            routes:
              - to: default
                via: 192.168.1.1
            nameservers:
              addresses: [8.8.8.8, 8.8.4.4]
```
- `netplan try`
- `netplan apply`


### Update
- `sudo apt update`
- `sudo apt upgrade`


### Install Git
- `sudo apt install git`
```
git --version
git version 2.43.0
```

### Install Python, pip, venv and other dependencies for Odoo
- `sudo apt install build-essential wget python3-pip python3-dev python3-venv python3-wheel libfreetype6-dev libxml2-dev libzip-dev libsasl2-dev python3-setuptools libjpeg-dev zlib1g-dev libpq-dev libxslt1-dev libldap2-dev libtiff5-dev libopenjp2-7-dev`

- **Odoo 17 documentation**
```
sudo apt install python3-pip libldap2-dev libpq-dev libsasl2-dev
```

- `python3 --version`
```
Python 3.12.3
```

- `pip3 --version`
```
pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)
```

### Install wkhtmltopdf for reports html to pdf
- `sudo apt install wkhtmltopdf`
```
wkhtmltopdf --version
wkhtmltopdf 0.12.6
```


### Install and configure PostgreSQL
- `sudo apt install postgresql postgresql-client`
- `sudo systemctl status postgresql.service`
```
● postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/usr/lib/systemd/system/postgresql.service; enabled; preset: enabled)
     Active: active (exited) since Wed 2024-09-11 07:59:47 UTC; 3h 1min ago
    Process: 18599 ExecStart=/bin/true (code=exited, status=0/SUCCESS)
   Main PID: 18599 (code=exited, status=0/SUCCESS)
        CPU: 3ms

de set. 11 07:59:47 ubuserver systemd[1]: Starting postgresql.service - PostgreSQL RDBMS...
de set. 11 07:59:47 ubuserver systemd[1]: Finished postgresql.service - PostgreSQL RDBMS.
```

- by default, the only user is **postgres**. As Odoo forbids connecting as postgres, create a new PostgreSQL user
- `sudo -u postgres createuser -d -R -S $USER`
- `createdb $USER`
- because the PostgreSQL user has the same name as the Unix login, it is possible to connect to the database without a password
- or if user linux and user postgresql have the same password

- connect to PostgreSQL
- `sudo -u postgres psql`
- `postgres=# \l`
```                                                       List of databases
   Name    |  Owner   | Encoding | Locale Provider |   Collate   |    Ctype    | ICU Locale | ICU Rules |   Access privileges
-----------+----------+----------+-----------------+-------------+-------------+------------+-----------+-----------------------
 aleon     | aleon    | UTF8     | libc            | ca_ES.UTF-8 | ca_ES.UTF-8 |            |           |
 postgres  | postgres | UTF8     | libc            | ca_ES.UTF-8 | ca_ES.UTF-8 |            |           |
 template0 | postgres | UTF8     | libc            | ca_ES.UTF-8 | ca_ES.UTF-8 |            |           | =c/postgres          +
           |          |          |                 |             |             |            |           | postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | ca_ES.UTF-8 | ca_ES.UTF-8 |            |           | =c/postgres          +
           |          |          |                 |             |             |            |           | postgres=CTc/postgres
```    
- `postgres=# \du`
```   
                             List of roles
 Role name |                         Attributes
-----------+------------------------------------------------------------
 aleon     | Create DB
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS
```

- create new password for *aleon* user, the same of the linux user
- `postgres=# ALTER USER aleon PASSWORD 'password';`

- **to activate remote connection for DBeaver in host**
- `sudo nano /etc/postgresql/16/main/postgresql.conf`
- **postgresql.conf**
```
...
#------------------------------------------------------------------------------
# CONNECTIONS AND AUTHENTICATION
#------------------------------------------------------------------------------

# - Connection Settings -

#listen_addresses = 'localhost'         # what IP address(es) to listen on;
                                        # comma-separated list of addresses;
                                        # defaults to 'localhost'; use '*' for all
                                        # (change requires restart)
listen_addresses = '*'
port = 5432                             # (change requires restart)
...
```

- `sudo nano /etc/postgresql/16/main/pg_hba.conf`
- **pg_hba.conf**
```
...
# Database administrative login by Unix domain socket
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
# host    all             all             127.0.0.1/32            scram-sha-256
host    all             all             0.0.0.0/0               md5
# IPv6 local connections:
#host    all             all             ::1/128                 scram-sha-256
host    all             all             ::/0                    md5
...
```

- `sudo systemctl restart postgresql`


### Install Odoo

- `git clone https://github.com/odoo/odoo.git --depth 1 --branch 17.0 odoo17`
- install dependencies with *venv* and *pip*
- `cd odoo17`
- `python3 -m venv venv`
- `source venv/bin/activate`
```
(venv) aleon@ubuserver:~/odoo17$
```
- `pip install -r requirements.txt`

### Run Odoo
- **Odoo 17 documentation**
```
python3 odoo-bin --addons-path=addons -d mydb
```
- to run first time without config file and force the creation of database
- `python3 odoo-bin -d aleon -i base`
- after execute
- `python3 odoo-bin -d aleon`
- or
- `python3 odoo-bin`
- to save the current configuration into a default file
- `python3 odoo-bin --save`
- the file will be save into `/home/aleon/.odoorc`

### Create congif file and run Odoo with this file
- `sudo nano odoo.conf`
```
[options]
; This is the password that allows database operations:
; admin_passwd = admin
db_host = False
db_port = False
db_user = aleon
;db_password = 
addons_path = addons/, custom/
default_productivity_apps = True
```
- `python3 odoo-bin -c odoo.conf -d aleon`
- or
- `python3 odoo-bin -c odoo.conf`


### Connect to Odoo with browser
- http://192.168.1.60:8069/



## Config Debug [debugpy] for VSCode

- `source venv/bin/activate`
- `pip install debugpy`

- create `.bin/debug.sh`
```
source venv/bin/activate
python3 /home/aleon/odoo17/venv/lib/python3.12/site-packages/debugpy --listen 0.0.0.0:5678 ./odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate --dev xml
```

- create `/home/aleon/odoo17/.vscode/launch.json`
```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Debugpy",
      "type": "python",
      "request": "attach",
      "port": 5678,
      "host": "localhost"
    }
  ]
}
```

- run `source .bin/debug.sh`

- to fix connections on port
```
lsof -i :5678
sudo kill -9 <process_id>
```



## Doc
- https://www.odoo.com/documentation/17.0/administration/on_premise/source.html
- https://www.cybrosys.com/blog/how-to-install-odoo-17-on-ubuntu-20-04-lts-server
- https://www.rosehosting.com/blog/how-to-install-odoo-17-on-ubuntu-22-04/
- https://stackoverflow.com/questions/12720967/how-can-i-change-a-postgresql-user-password
- https://stackoverflow.com/questions/18580066/how-to-allow-remote-access-to-postgresql-database
- https://github.com/odoo/documentation/issues/1837