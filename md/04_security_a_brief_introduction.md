# Chapter 4: Security - A Brief Introduction

https://www.odoo.com/documentation/17.0/developer/tutorials/restrict_data_access.html

- Odoo provides a security mechanism to allow access to the data for specific groups of users


## Data Files (CSV)

- Odoo is a highly data driven system
- Although behavior is customized using Python code, part of a module’s value is in the data it sets up when loaded
- One way to load data is through a *CSV* file
- One example is the list of country states which is loaded at installation of the base module

```
"id","country_id:id","name","code"
state_au_1,au,"Australian Capital Territory","ACT"
state_au_2,au,"New South Wales","NSW"
state_au_3,au,"Northern Territory","NT"
state_au_4,au,"Queensland","QLD"
...
```

- `id` is an *external identifier*. It can be used to refer to the record (without knowing its in-database identifier)
- https://www.odoo.com/documentation/17.0/developer/glossary.html#term-external-identifier
- `country_id:id` refers to the country by using its *external identifier*
- `name` is the name of the state.
- `code` is the code of the state.

- These three fields are defined in the `res.country.state` model.
- By convention, a file importing data is located in the `data` folder of a module. 
- When the data is related to security, it is located in the `security` folder 
- When the data is related to views and actions, it is located in the `views` folder
- Additionally, all of these files must be declared in the data list within the `__manifest__.py` file
- Our example file is defined in the manifest of the **base** module.

```
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Base',
    'version': '1.3',
    'category': 'Hidden',
    'description': """
The kernel of Odoo, needed for all installation.
===================================================
""",
    'depends': [],
    'data': [
        'data/res.lang.csv',
        'data/res_lang_data.xml',
...
        'data/res_country_data.xml',
...
        'data/res.country.state.csv',
...
```

- The data files are sequentially loaded following their order in the `__manifest__.py` file
- This means that if data A refers to data B, you must make sure that B is loaded before A
- In the case of the country states, you will note that the list of countries is loaded before the list of country states
- This is because the states refer to the countries


## Access Rights

https://www.odoo.com/documentation/17.0/developer/reference/backend/security.html#reference-security-acl

- When no access rights are defined on a model, Odoo determines that no users can access the data. It is even notified in the log:

```
WARNING rd-demo odoo.modules.loading: The models ['estate.property'] have no access rules in module estate, consider adding some, like:
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

- Access rights are defined as records of the model `ir.model.access`
- Each access right is associated with a model, a group (or no group for global access) and a set of permissions: create, read, write and unlink (delete)
- Such access rights are usually defined in a CSV file named `ir.model.access.csv`

- Here is an example for our previous test_model:
```
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
access_test_model,access_test_model,model_test_model,base.group_user,1,0,0,0
```

- **id** is an external identifier.
- **name** is the name of the `ir.model.access`.
- **model_id/id** refers to the model which the access right applies to. The standard way to refer to the model is `model_<model_name>`, where `<model_name>` is the `_name` of the model with the `.` replaced by `_`. Seems cumbersome? Indeed it is…
- **group_id/id** refers to the *group* which the access right applies to
- **perm_read**,**perm_write**,**perm_create**,**perm_unlink**: read, write, create and unlink permissions


## Add access rights to the model estate_property

- `cd ~/odoo17/tutorials/estate`
- `mkdir security`
- `touch security/ir.model.access.csv`

```
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
access_estate_property,access_estate_property,model_estate_property,base.group_user,1,1,1,1
```

- restart Odoo
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate`