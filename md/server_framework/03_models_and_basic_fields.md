# Chapter 3: Models And Basic Fields

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/03_basicmodel.html


- ⚠️ Do not use mutable global variables.
A single Odoo instance can run several databases in parallel within the same python process. Distinct modules might be installed on each of these databases, therefore we cannot rely on global variables that would be updated depending on installed modules.

## Object-Relational Mapping
https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#reference-orm-model

- A key component of Odoo is the *ORM layer*
- This layer avoids having to manually write most SQL and provides extensibility and security services.
- Business objects are declared as Python classes extending **Model**, which integrates them into the automated persistence system
- *Models* can be configured by setting *attributes* in their definition. The most important attribute is **_name**, which is required and defines the name for the model in the Odoo system.

```
from odoo import models

class TestModel(models.Model):
    _name = "test_model"
```

- This definition is enough for the ORM to generate a database table named `test_model`. 
- By convention all models are located in a **models** directory and each model is defined in its own Python file.


## Creating Model [Estate Property]

- cd `/home/aleon/odoo17/tutorials/estate`
- `mkdir models`
- create model `touch models/estate_property.py`
```
from odoo import models

class EstateProperty(models.Model):
    _name = "estate.property"
```

- import model `touch models/__init__.py`
```
# -*- coding: utf-8 -*-

from . import estate_property
```

- import folder models in `__init__.py`
```
# -*- coding: utf-8 -*-

from . import models
```

- restart Odoo
- when we restart the server, we will add the parameters `-d` and `-u`
- you can use the `-i` or `--init` flag instead of the `-u` `or `--upgrade` flag
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -i estate`
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate`

- ⚠️ he necessitat `-i` la 1a vegada per tal de crear-se la taula
- `-u estate` means we want to upgrade the *estate* module, i.e. the ORM will apply database schema changes. In this case it creates a new table
- `-d rd-demo` means that the upgrade should be performed on the *rd-demo* database
- `-u` should always be used in combination with `-d`

```
$ psql -d rd-demo
rd-demo=# SELECT COUNT(*) FROM estate_property;
count
-------
    0
(1 row)
```


## Model fields
https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#reference-orm-fields

- *Fields* are used to define what the model can store and where they are stored
- *Fields* are defined as *attributes* in the model class

```
from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"

    name = fields.Char()
```

- The name field is a *Char* which will be represented as a Python unicode str and a SQL VARCHAR

- There are two broad categories of fields: **simple** fields, which are atomic values stored directly in the model’s table, 
and **relational** fields, which link records (of the same or different models).

- Simple field examples are *Boolean*, *Float*, *Char*, *Text*, *Date* and *Selection*.
- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.fields.Selection


## Add basic fields to the Real Estate Property table

- **tutorials/estate/models/estate_property.py**
```py
from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "descripció del model propietat immobilària"

    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
        help="Type is used to indicate one of the four main points of the compass"
    )
```

- restart Odoo
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate`

```
$ psql -d rd-demo
rd-demo=# \d estate_property;
                                            Table "public.estate_property"
       Column       |            Type             | Collation | Nullable |                   Default
--------------------+-----------------------------+-----------+----------+---------------------------------------------
 id                 | integer                     |           | not null | nextval('estate_property_id_seq'::regclass)
 create_uid         | integer                     |           |          |
 write_uid          | integer                     |           |          |
 create_date        | timestamp without time zone |           |          |
 write_date         | timestamp without time zone |           |          |
 bedrooms           | integer                     |           |          |
 living_area        | integer                     |           |          |
 facades            | integer                     |           |          |
 garden_area        | integer                     |           |          |
 name               | character varying           |           |          |
 postcode           | character varying           |           |          |
 garden_orientation | character varying           |           |          |
 date_availability  | date                        |           |          |
 description        | text                        |           |          |
 garage             | boolean                     |           |          |
 garden             | boolean                     |           |          |
 expected_price     | double precision            |           |          |
 selling_price      | double precision            |           |          |
Indexes:
    "estate_property_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "estate_property_create_uid_fkey" FOREIGN KEY (create_uid) REFERENCES res_users(id) ON DELETE SET NULL
    "estate_property_write_uid_fkey" FOREIGN KEY (write_uid) REFERENCES res_users(id) ON DELETE SET NULL
```


## Common Attributes

```
name = fields.Char(required=True)
```

Some attributes are available on all fields, here are the most common ones:

- **`string` (str, default: field’s name)**
The label of the field in UI (visible by users).

- **`required` (bool, default: False)**
If True, the field can not be empty. It must either have a default value or always be given a value when creating a record.

- **`help` (str, default: '')**
Provides long-form help tooltip for users in the UI.

- **`index` (bool, default: False)**
Requests that Odoo create a database index on the column.


- **tutorials/estate/models/estate_property.py**
```py
from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "descripció del model propietat immobilària"

    name = fields.Char(
        required=True
    )
...
    expected_price = fields.Float(
        required=True
    )
...
```

```
$ psql -d rd-demo
rd-demo=# \d estate_property;
                                            Table "public.estate_property"
    Column       |            Type             | Collation | Nullable |                   Default
--------------------+-----------------------------+-----------+----------+---------------------------------------------
...
name               | character varying           |           | not null |
...
expected_price     | double precision            |           | not null |
...
```


## Automatic Fields

- You may have noticed your model has a few fields you never defined. Odoo creates a few fields in all models
- These fields are managed by the system and can’t be written to, but they can be read if useful or necessary

- **`id` (Id)**
The unique identifier for a record of the model

- **`create_date` (Datetime)**
Creation date of the record

- **`create_uid` (Many2one)**
User who created the record

- **`write_date` (Datetime)**
Last modification date of the record

- **`write_uid` (Many2one)**
User who last modified the record

- it is possible to *disable* the automatic creation of some fields
- writing raw SQL queries is possible, but requires caution as this bypasses all Odoo authentication and security mechanisms