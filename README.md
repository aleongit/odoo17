## Introduction

Checkpoints:

- install Odoo 17 on-premise with Source install on Ubuntu Server 24.04.1 LTS




## Run

- cd odoo17
- source venv/bin/activate
- python3 odoo-bin -c odoo.conf
- http://192.168.1.60:8069/




## Requeriments / Prerequisites

OS: Ubuntu noble 24.04 x86_64
Host: VMware Virtual Platform
Kernel: Linux 6.8.0-41-generic

🖥️ lsb_release -a
→
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 24.04.1 LTS
Release:        24.04
Codename:       noble

🖥️ git --version
→ git version 2.43.0

🖥️ python3 --version
→ Python 3.12.3

🖥️ pip3 --version
→ pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)

🖥️ sudo -u postgres psql
→ psql (16.4 (Ubuntu 16.4-0ubuntu0.24.04.2))




## Dependencies

- python3-pip
- python3-venv
- wkhtmltopdf (HTML to PDF)
- others




## Dev environment

- **host**
- Microsoft Windows [Versión 10.0.19045.4780]
- Visual Studio Code 1.93.0
- Visual Studio Extension > `Remote Explorer` for SSH
- VMware® Workstation 17 Player [17.5.2 build-23775571]
- DBeaver [Version 24.2.0.202409011551]

- **virtual host**
- Ubuntu Server 24.04.1 LTS



## Project Steps

- **test** 




## Doc
- https://www.odoo.com/documentation/17.0/administration/on_premise/source.html