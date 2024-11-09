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