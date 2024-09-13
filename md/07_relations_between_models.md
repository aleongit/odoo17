# Chapter 7: Relations Between Models

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/07_relations.html

- The previous chapter covered the creation of custom views for a model containing basic fields. However, in any real business scenario we need more than one model. Moreover, links between models are necessary. One can easily imagine one model containing the customers and another one containing the list of users. You might need to refer to a customer or a user on any existing business model

In our real estate module, we want the following information for a property:

- the customer who bought the property
- the real estate agent who sold the property
- the property type: house, apartment, penthouse, castle…
- a list of tags characterizing the property: cozy, renovated…
- a list of the offers received 

## Many2one

- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.fields.Many2one

- In our real estate module, we want to define the concept of *property type*. A property type is, for example, a house or an apartment. It is a standard business need to categorize properties according to their type, especially to refine filtering

- A property can have one type, but the same type can be assigned to many properties. This is supported by the **many2one** concept

- A many2one is a simple link to another object. For example, in order to define a link to the res.partner in our test model, we can write:
```
partner_id = fields.Many2one("res.partner", string="Partner")
```

- By convention, many2one fields have the `_id` suffix. Accessing the data in the partner can then be easily done with:
```
print(my_test_object.partner_id.name)
```

- https://www.postgresql.org/docs/12/tutorial-fk.html

- In practice a many2one can be seen as a dropdown list in a form view

## Add the Real Estate Property Type table.

- Create the `estate.property.type` model
- Add the menus
- Add the field `property_type_id` into your `estate.property` model and its form, tree and search views

- creem 2n model
- `cd ~/odoo17/tutorials/estate/`
- `touch models/estate_property_type.py`
```
from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "tipus de propietat immobiliària"

    name = fields.Char(
        string="Name",
        required=True
    )
```

- afegim 2n model a models
- **tutorials/estate/models/__init__.py**
```
# -*- coding: utf-8 -*-

from . import estate_property
from . import estate_property_type
```

- creem un nou fitxer separat per les accions dels 2 models
- `touch views/estate_actions.xml`
```
<?xml version="1.0"?>
<odoo>
    <!-- action estate.property -->
    <record id="estate.property_action" model="ir.actions.act_window">
        <field name="name">Properties</field>
        <field name="res_model">estate.property</field>
        <field name="view_mode">tree,form</field>
    </record>

    <!-- action estate.property.type -->
    <record id="estate.property_type_action" model="ir.actions.act_window">
        <field name="name">Properties Types</field>
        <field name="res_model">estate.property.type</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

- afegim 2n menú pel 2n model
- **tutorials/estate/views/estate_menus.xml**
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <menuitem id="estate_property_menu_root" name="Real Estate">
        <!--Advertisements -->
        <menuitem id="estate_property_first_level_menu" name="Advertisements">
            <menuitem id="estate_property_model_menu_action" action="estate.property_action"/>
        </menuitem>

        <!--Settings -->
        <menuitem id="estate_property_type_first_level_menu" name="Settings">
            <menuitem id="estate_property_type_model_menu_action" action="estate.property_type_action"/>
        </menuitem>
    </menuitem>
</odoo>
```

- creem vistes pel 2n model
- `touch views/estate_property_type_views.xml`
```
<?xml version="1.0"?>
<odoo>

    <!-- list -->
    <record id="estate.property_type_list" model="ir.ui.view">
        <field name="name">Property Type List</field>
        <field name="model">estate.property.type</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name" string="Type" />
            </tree>
        </field>
    </record>

    <!-- form -->
    <record id="estate.property_type_form" model="ir.ui.view">
        <field name="name">Property Type Form</field>
        <field name="model">estate.property.type</field>
        <field name="arch" type="xml">
            <form string="Test">
                <sheet>
                    <h1>
                        <field name="name"/>
                    </h1>
                </sheet>
            </form>
        </field>
    </record>

    <!-- search -->
    <record id="estate.property_type_search" model="ir.ui.view">
        <field name="name">estate.property.type.search</field>
        <field name="model">estate.property.type</field>
        <field name="arch" type="xml">
            <search string="Busca...">
                <field name="name" string="Type" />
            </search>
        </field>
    </record>


</odoo>
```

- afegim camp relacionat al 1r model
- **tutorials/estate/models/estate_property.py**
```
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "descripció del model propietat immobilària"

    # reserved fields (name, active, state)
    name = fields.Char(
        string="Name",
        required=True
    )
...
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
```

- afegim camp a les vistes del 1r model
- **tutorials/estate/views/estate_property_views.xml**
```
<field name="property_type_id"/>
```

- afegim fitxers a manifest
- **tutorials/estate/__manifest__.py**
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
    'data': [
        # data
        # views
        'views/estate_actions.xml',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        # access
        'security/ir.model.access.csv',
    ],
    # data files containing optionally loaded demonstration data
    # 'demo': ['demo/demo_data.xml',],
}
```

- afegim permisos pel 2n model
- **tutorials/estate/security/ir.model.access.csv**
```
id,name,model_id/id,group_id/id,perm_read,perm_write,perm_create,perm_unlink
access_estate_property,access_estate_property,model_estate_property,base.group_user,1,1,1,1
access_estate_property_type,access_estate_property_type,model_estate_property_type,base.group_user,1,1,1,1
```

- In the real estate module, there are still two missing pieces of information we want on a property: the *buyer* and the *salesperson*. The buyer can be any individual, but on the other hand the salesperson must be an employee of the real estate agency (i.e. an Odoo user)

- In Odoo, there are two models which we commonly refer to
- `res.partner`: a partner is a physical or legal entity. It can be a company, an individual or even a contact address
- `res.users`: the users of the system. Users can be ‘internal’, i.e. they have access to the Odoo backend. Or they can be ‘portal’, i.e. they cannot access the backend, only the frontend (e.g. to access their previous orders in eCommerce)

## Add the buyer and the salesperson in the model

- Add a *buyer* and a *salesperson* to the `estate.property` model using the two common models mentioned above. They should be added in a new tab of the form view
- The default value for the salesperson must be the current user. The buyer should not be copied

The object `self.env` gives access to request parameters and other useful things:

- `self.env.cr` or `self._cr` is the database cursor object; it is used for querying the database
- `self.env.uid` or `self._uid` is the current user’s database id
- `self.env.user` is the current user’s record
- `self.env.context` or `self._context` is the context dictionary
- `self.env.ref(xml_id)` returns the record corresponding to an XML id
- `self.env[model_name]` returns an instance of the given model


- **tutorials/estate/models/estate_property.py**
```
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "descripció del model propietat immobilària"

    # reserved fields (name, active, state)
    name = fields.Char(
        string="Name",
        required=True
    )
...
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, default=lambda self: self.env.user)
```

- **tutorials/estate/views/estate_property_views.xml**
```
    <!-- form -->
    <record id="estate.property_form" model="ir.ui.view">
        <field name="name">Property</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <form string="Test">
...
                    <notebook>
                        <!-- pag description -->
                        <page string="Description">
                            <group>
                                <field name="description"/>
                                <field name="bedrooms"/>
                                <field name="living_area" string="Living Area (sqm)"/>
                                <field name="facades"/>
                                <field name="garage"/>
                                <field name="garden"/>
                                <field name="garden_area" string="Garden Area (sqm)"/>
                                <field name="garden_orientation"/>
                            </group>
                        </page>
                        <!-- pag other info -->
                        <page string="Other Info">
                            <group>
                                <field name="salesperson_id" string="Salesman"/>
                                <field name="buyer_id" string="Buyer"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
```


## Many2many

https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.fields.Many2many

- In our real estate module, we want to define the concept of property tags. A property tag is, for example, a property which is ‘cozy’ or ‘renovated’

- A property can have many tags and a tag can be assigned to many properties. This is supported by the **many2many** concept

- A *many2many* is a bidirectional multiple relationship: any record on one side can be related to any number of records on the other side. For example, in order to define a link to the account.tax model on our test model, we can write:

```
tax_ids = fields.Many2many("account.tax", string="Taxes")
```

- By convention, *many2many* fields have the `_ids` suffix. This means that several taxes can be added to our test model. It behaves as a list of records, meaning that accessing the data must be done in a loop:
```
for tax in my_test_object.tax_ids:
    print(tax.name)
```

- A list of records is known as a `recordset`, i.e. an ordered collection of records. It supports standard Python operations on collections, such as `len()` and `iter()`, plus extra set operations like `recs1` | `recs2`

## Add the Real Estate Property Tag table

- Create the *estate.property.tag* model and add the following field
- name (Char) *required
- Add the menus
- Add the field *tag_ids* to your *estate.property model* and in its form and tree views
- Tip: in the view, use the `widget="many2many_tags"` attribute

------------------

- create model in `tutorials/estate/models/estate_property_tag.py`
- add many2many field in `tutorials/estate/models/estate_property.py`
```
tag_ids = fields.Many2many("estate.property.tag", string="Tags")
```
- add model in models `tutorials/estate/models/__init__.py`
- add action tag in `tutorials/estate/views/estate_actions.xml`
- add menu tag in `tutorials/estate/views/estate_menus.xml`
- create views in `tutorials/estate/views/estate_property_tag_views.xml`
- add field in `tutorials/estate/views/estate_property_views.xml`
- add access in `tutorials/estate/security/ir.model.access.csv`
- add files in `tutorials/estate/__manifest__.py`


