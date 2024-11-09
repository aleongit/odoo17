# Chapter 11: Add The Sprinkles

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/11_sprinkles.html

Our real estate module now makes sense from a business perspective. We created specific views, added several action buttons and constraints. However our user interface is still a bit rough. We would like to add some colors to the list views and make some fields and buttons conditionally disappear. For example, the ‘Sold’ and ‘Cancel’ buttons should disappear when the property is sold or canceled since it is no longer allowed to change the state at this point.

This chapter covers a very small subset of what can be done in the views. Do not hesitate to read the reference documentation for a more complete overview.

Reference: the documentation related to this chapter can be found in View records and View architectures.

https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_records.html

https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_architectures.html


## Inline Views

- Goal: at the end of this section, a specific list of properties should be added to the property type view

- In the real estate module we added a list of offers for a property. We simply added the field `offer_ids` with:
```
<field name="offer_ids"/>
```

- The field uses the specific view for `estate.property.offer`
- In some cases we want to define a specific list view which is only used in the context of a form view. For example, we would like to display the list of properties linked to a property type. However, we only want to display 3 fields for clarity: name, expected price and state.
- To do this, we can define inline list views. An inline list view is defined directly inside a form view. For example:
```
from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"

    description = fields.Char()
    line_ids = fields.One2many("test_model_line", "model_id")


class TestModelLine(models.Model):
    _name = "test_model_line"
    _description = "Test Model Line"

    model_id = fields.Many2one("test_model")
    field_1 = fields.Char()
    field_2 = fields.Char()
    field_3 = fields.Char()
```

```
<form>
    <field name="description"/>
    <field name="line_ids">
        <tree>
            <field name="field_1"/>
            <field name="field_2"/>
        </tree>
    </field>
</form>
```

- In the form view of the test_model, we define a specific list view for `test_model_line` with fields `field_1` and `field_2`

- Exercise: Add an inline list view
- Add the One2many field `property_ids` to the `estate.property.type` model
- Add the field in the `estate.property.type` form view as depicted in the Goal of this section

- **tutorials/estate/models/estate_property_type.py**
```
property_ids = fields.One2many("estate.property", "property_type_id")
```

- **tutorials/estate/views/estate_property_type_views.xml**
```
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
                    <notebook>
                        <!-- pag properties -->
                        <page string="Properties">
                            <field name="property_ids">
                                <tree>
                                    <field name="name"/>
                                    <field name="expected_price"/>
                                    <field name="state"/>
                                </tree>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
```

## Widgets

Reference: the documentation related to this section can be found in Fields.

https://www.odoo.com/documentation/17.0/developer/reference/frontend/javascript_reference.html#reference-js-widgets


- **Goal**: at the end of this section, the state of the property should be displayed using a specific widget
- Four states are displayed: New, Offer Received, Offer Accepted and Sold

- Whenever we've added fields to our models, we've (almost) never had to worry about how these fields would look like in the user interface.
For example, a date picker is provided for a Date field and a One2many field is automatically displayed as a list.
Odoo chooses the right **widget** depending on the field type.

- However, in some cases, we want a specific representation of a field which can be done thanks to the widget attribute.
We already used it for the `tag_ids` field when we used the `widget="many2many_tags"` attribute. 
If we hadn't used it, then the field would have displayed as a list.

- Each field type has a set of widgets which can be used to fine tune its display. Some widgets also take extra options. 
An exhaustive list can be found in Fields.

- **Exercise**:
- Use the `status bar` widget
- Use the statusbar widget in order to display the `state` of the `estate.property` as depicted in the Goal of this section
- Warning: Same field multiple times in a view
- Add a field only once to a list or a form view. Adding it multiple times is not supported

- **tutorials/estate/views/estate_property_views.xml**
```
<!-- form -->
    <record id="estate.property_form" model="ir.ui.view">
        <field name="name">Property</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <form string="Test">
                <!-- header buttons -->
                <header>
                    <!-- actions -->
                    <button name="action_set_sold" type="object" string="Sold"/>
                    <button name="action_set_canceled" type="object" string="Canceled"/>
                    <!-- widget -->
                    <field name="state" widget="statusbar" statusbar_visible="new,offer_received,offer_accepted,sold"/>
                </header>
...
```

## List Order

Reference: the documentation related to this section can be found in Models.

https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#reference-orm-models

- **Goal**: at the end of this section, all lists should display by default in a deterministic order. Property types can be ordered manually

- During the previous exercises, we created several list views. However, at no point did we specify which order the records had to be listed in by default. This is a very important thing for many business cases. For example, in our real estate module we would want to display the highest offers on top of the list


### Model

- Odoo provides several ways to set a default order. The most common way is to define the `_order` attribute directly in the model. This way, the retrieved records will follow a deterministic order which will be consistent in all views including when records are searched programmatically. By default there is no order specified, therefore the records will be retrieved in a non-deterministic order depending on PostgreSQL

- The `_order` attribute takes a string containing a list of fields which will be used for sorting. It will be converted to an order_by clause in SQL. For example:
```
from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"
    _order = "id desc"

    description = fields.Char()
```

- Our records are ordered by descending `id`, meaning the highest comes first

- **Exercise**: Add model ordering
- Define the following orders in their corresponding models:
- estate.property >> Descending ID
- estate.property.offer >> Descending Price
- estate.property.tag >> Name
- estate.property.type >> Name

- **tutorials/estate/models/estate_property.py**
```
class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "descripció del model propietat immobilària"
    _order = "id desc"
...
```

- **tutorials/estate/models/estate_property_offer.py**
```
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "oferta de la propietat immobiliària"
    _order = "price desc"
...
```

- **tutorials/estate/models/estate_property_tag.py**
```
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "tag de propietat immobiliària"
    _order = "name"
...
```

- **tutorials/estate/models/estate_property_type.py**
```
class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "tipus de propietat immobiliària"
    _order = "name"
...
```


