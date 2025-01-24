# Chapter 2: A New Application

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/02_newapp.html


## The Real Estate Advertisement module

## Prepare the addon directory
- `mkdir tutorials/estate`
- the module must contain at least 2 files: the `__manifest__.py` file and a `__init__.py`
- `cd tutorials/estate`
- `touch __init__.py` (can remain empty)
- `touch __manifest__.py` (cannot remain empty. Its only required field is the **name**)

- In addition to providing the description of the module (name, category, summary, website…), it lists its *dependencies* (depends)
-  A *dependency* means that the Odoo framework will ensure that these modules are installed before our module is installed
-  The `__manifest__.py` file should only define the name and the dependencies of our modules. The only necessary framework module for now is **base**.
- https://www.odoo.com/documentation/17.0/developer/reference/backend/module.html#reference-module-manifest

-  nano `__manifest__.py`
```
# -*- coding: utf-8 -*-
# tutorial
{
    'name': "Real Estate",
    'version': '1.0',
    'license': 'AGPL-3',
    'depends': ['base'],
    'author': "aleon",
    'category': 'Test',
    'description': "Description of Real Estate",
    # data files always loaded at installation
    # 'data': ['views/mymodule_view.xml',],
    # data files containing optionally loaded demonstration data
    # 'demo': ['demo/demo_data.xml',],
}
```

- restart the Odoo server and go to Apps
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo`
- click on Update Apps List, search for estate and… tadaaa, your module appears!