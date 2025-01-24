# Chapter 5: Finally, Some UI To Play With

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/05_firstui.html


## Data Files (XML)
https://www.odoo.com/documentation/17.0/developer/reference/backend/data.html#reference-data

- In Chapter 4: Security - A Brief Introduction, we added data through a CSV file
- The CSV format is convenient when the data to load has a simple format
- When the format is more complex (e.g. load the structure of a view or an email template), we use the XML format
- For example, this help field contains HTML tags. While it would be possible to load such data through a CSV file, it is more convenient to use an XML file

- The XML files must be added to the same folders as the CSV files and defined similarly in the `__manifest__.py`
- The content of the data files is also sequentially loaded when a module is installed or updated, therefore all remarks made for CSV files hold true for XML files
- When the data is linked to views, we add them to the **views** folder

- ⚠️ When performance is important, the CSV format is preferred over the XML format. This is the case in Odoo where loading a CSV file is faster than loading an XML file

- In Odoo, the user interface (actions, menus and views) is largely defined by creating and composing records defined in an XML file
- A common pattern is **Menu > Action > View**. 
- To access records the user navigates through several menu levels; the deepest level is an action which triggers the opening of a list of the records


## Actions
https://www.odoo.com/documentation/17.0/developer/reference/backend/actions.html

- **Goal**: at the end of this section, an action should be loaded in the system. We won’t see anything yet in the UI, but the file should be loaded in the log:
```
INFO rd-demo odoo.modules.loading: loading estate/views/estate_property_views.xml
```

- Actions can be triggered in three ways:

1. by clicking on menu items (linked to specific actions)
2. by clicking on buttons in views (if these are connected to actions)
3. as contextual actions on object

```
<record id="test_model_action" model="ir.actions.act_window">
    <field name="name">Test action</field>
    <field name="res_model">test_model</field>
    <field name="view_mode">tree,form</field>
</record>
```

- `id` is an external identifier. It can be used to refer to the record (without knowing its in-database identifier).
- `model` has a fixed value of `ir.actions.act_window` (Window Actions (ir.actions.act_window))
- https://www.odoo.com/documentation/17.0/developer/reference/backend/actions.html#reference-actions-window
- `name` is the name of the action
- `res_model` is the model which the action applies to
- `view_mode` are the views that will be available; in this case they are the list (tree) and form views


## Add Action for Estate Property model

- `cd ~/odoo17/tutorials/estate/`
- `mkdir views`
- `touch views/estate_property_views.xml`

```
<?xml version="1.0"?>
<odoo>    <!--  -->
    <record id="estate.property_action" model="ir.actions.act_window">
        <field name="name">Properties</field>
        <field name="res_model">estate.property</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

- add in `__manifest__.py`
```
    'data': [
        'views/estate_property_views.xml',
        'security/ir.model.access.csv',
    ],
```

- restart Odoo
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate`
```
2024-09-12 15:42:23,029 18360 INFO rd-demo odoo.modules.loading: loading estate/views/estate_property_views.xml
```

## Menus

https://www.odoo.com/documentation/17.0/developer/reference/backend/data.html#reference-data-shortcuts

- To reduce the complexity in declaring a menu (ir.ui.menu) and connecting it to the corresponding action, we can use the `<menuitem>` shortcut

A basic menu for our test_model_action is:
```
<menuitem id="test_model_menu_action" action="test_model_action"/>
```

- The menu *test_model_menu_action* is linked to the action *test_model_action*, and the action is linked to the model *test_model*
- As previously mentioned, the action can be seen as the link between the menu and the model

- However, menus always follow an architecture, and in practice there are three levels of menus:
1. The root menu, which is displayed in the App switcher (the Odoo Community App switcher is a dropdown menu)
2. The first level menu, displayed in the top bar
3. The action menus

- The easiest way to define the structure is to create it in the XML file 
- A basic structure for our test_model_action is:
```
<menuitem id="test_menu_root" name="Test">
    <menuitem id="test_first_level_menu" name="First Level">
        <menuitem id="test_model_menu_action" action="test_model_action"/>
    </menuitem>
</menuitem>
```
- The name for the third menu is taken from the name of the action


## Create Menus for Estate Property model

- `cd ~/odoo17/tutorials/estate/`
- `mkdir views`
- `touch views/estate_menus.xml`

```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <menuitem id="estate_property_menu_root" name="Real Estate">
        <menuitem id="estate_property_first_level_menu" name="Advertisements">
            <menuitem id="estate_property_model_menu_action" action="estate.property_action"/>
        </menuitem>
    </menuitem>
</odoo>
```

- add in `__manifest__.py`
```
    'data': [
        # data
        # views
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        # access
        'security/ir.model.access.csv',
    ],
```

- restart Odoo
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate`


## Fields, Attributes And View

- So far we have only used the generic view for our real estate property advertisements, but in most cases we want to fine tune the view 
- There are many fine-tunings possible in Odoo, but usually the first step is to make sure that:

1. some fields have a default value
2. some fields are read-only
3. some fields are not copied when duplicating the record


## Some New Attributes

- Before moving further with the view design, let’s step back to our model definition
- We saw that some attributes, such as `required=True`, impact the table schema in the database
- Other attributes will impact the view or provide default values
- Find the appropriate attributes (**Field**) to:
- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.fields.Field

- **tutorials/estate/models/estate_property.py**
```
    selling_price = fields.Float(
        readonly=True,
        copy=False
    )
```


## Default Values

- Any field can be given a *default value*
- In the field definition, add the option default=X where X is either a Python literal value (boolean, integer, float, string) or a function taking a model and returning a value:

```
name = fields.Char(default="Unknown")
last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
```

- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.fields.Date.today


- **tutorials/estate/models/estate_property.py**
```
from odoo.tools import date_utils
...

    date_availability = fields.Date(
        copy=False,
        default=date_utils.add(fields.date.today(), months=3)
    )
    bedrooms = fields.Integer(
        default=2
    )
```


## Reserved Fields

https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#reference-orm-fields-reserved

- A few field names are *reserved* for pre-defined behaviors. 
- They should be defined on a model when the related behavior is desired
- for example **name**, **active**, **state**

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
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                   ('offer_accepted', 'Offer Accepted'), ('sold ', 'Sold '),
                   ('canceled', 'Canceled')],
        required=True,
        copy=False,
        default="new"
    )
```



