# Chapter 11: Inheritance

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/12_inheritance.html

A powerful aspect of Odoo is its modularity. A module is dedicated to a business need, but modules can also interact with one another. This is useful for extending the functionality of an existing module. For example, in our real estate scenario we want to display the list of a salesperson’s properties directly in the regular user view.

But before going through the specific Odoo module inheritance, let’s see how we can alter the behavior of the standard *CRUD* (Create, Retrieve, Update or Delete) methods.

## Python Inheritance

- **Goal**: at the end of this section:
- It should not be possible to delete a property which is not new or canceled
- When an offer is created, the property state should change to ‘Offer Received’
- It should not be possible to create an offer with a lower price than an existing offer

---

In our real estate module, we never had to develop anything specific to be able to do the standard CRUD actions. The Odoo framework provides the necessary tools to do them. In fact, such actions are already included in our model thanks to classical Python inheritance:
```
from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"

    ...
```

- Our `class TestModel` inherits from `Model` which provides `create()`, `read()`, `write()` and `unlink()`

- These methods (and any other method defined on `Model`) can be extended to add specific business logic:
```
from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"

    ...

    @api.model
    def create(self, vals):
        # Do some business logic, modify vals...
        ...
        # Then call super to execute the parent method
        return super().create(vals)
```

- The decorator `model()` is necessary for the `create()` method because the content of the recordset self is not relevant in the context of creation, but it is not necessary for the other CRUD methods

- It is also important to note that even though we can directly override the `unlink()` method, you will almost always want to write a new method with the decorator `ondelete()` instead. Methods marked with this decorator will be called during `unlink()` and avoids some issues that can occur during uninstalling the model’s module when `unlink()` is directly overridden

- In Python 3, `super()` is equivalent to `super(TestModel, self)`
- The latter may be necessary when you need to call the parent method with a modified recordset

- ⚠️ **Danger**:
- It is very important to always call `super()` to avoid breaking the flow
- There are only a few very specific cases where you don’t want to call it
- Make sure to always return data consistent with the parent method
- For example, if the parent method returns a `dict()`, your override must also return a `dict()`

---

- **Exercise**: Add business logic to the CRUD methods
- Prevent deletion of a property if its state is not ‘New’ or ‘Canceled’
- *Tip*: create a new method with the `ondelete()` decorator and remember that `self` can be a recordset with more than one record
- At offer creation, set the property state to ‘Offer Received’
- Also raise an error if the user tries to create an offer with a lower amount than an existing offer
- *Tip*: the `property_id` field is available in the `vals`, but it is an `int`
- To instantiate an `estate.property` object, use `self.env[model_name].browse(value)`

---

- **tutorials/estate/models/estate_property.py**
```
def unlink(self):
    for record in self:
        if record.state not in ('new', 'canceled'):
            raise UserError('Only new or cancelled properties can be deleted')
    return super().unlink()
```

- **tutorials/estate/models/estate_property_offer.py**
```
@api.model
def create(self, vals):
    property = self.env['estate.property'].browse(vals['property_id'])
    if property.state in ('offer_accepted', 'sold', 'canceled'):
        raise UserError(
            'It is not allowed to create offers if the property has an accepted offer, is sold or cancelled')
    if vals['price'] <= property.best_price:
        raise UserError(f'The offer must be higher than {
                        property.best_price}')
    property.state = 'offer_received'
    return super(EstatePropertyOffer, self).create(vals)
```

## Model Inheritance

- **Reference**: the documentation related to this topic can be found in Inheritance and extension
- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#reference-orm-inheritance

- In our real estate module, we would like to display the list of properties linked to a salesperson directly in the Settings / Users & Companies / Users form view
- To do this, we need to add a field to the `res.users` model and adapt its view to show it
- Odoo provides two inheritance mechanisms to extend an existing model in a modular way

The first inheritance mechanism allows modules to modify the behavior of a model defined in an another module by:
- adding fields to the model
- overriding the definition of fields in the model
- adding constraints to the model
- adding methods to the model
- overriding existing methods in the model

The second inheritance mechanism (delegation) allows every record of a model to be linked to a parent model’s record and provides transparent access to the fields of this parent record

![Screenshot](../md/inheritance_methods.png)

- In Odoo, the first mechanism is by far the most used
- In our case, we want to add a field to an existing model, which means we will use the first mechanism. For example:
```
from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "inherited.model"

    new_field = fields.Char(string="New Field")
```

- By convention, each inherited model is defined in its own Python file
- In our example, it would be `models/inherited_model.py`

---

- **Exercise**: Add a field to Users
- Add the following field to `res.users`:
- *Field*: property_ids
- *Type*: One2many inverse of the field that references the salesperson in `estate.property`
- Add a *domain* to the field so it only lists the available properties

- **tutorials/estate/models/res_users.py**
```
from odoo import fields, models


class ResUsers(models.Model):

    _inherit = 'res.users'

    # one2many
    property_ids = fields.One2many(
        comodel_name='estate.property', inverse_name='salesperson_id',
        domain=[('state', 'in', ['new', 'offer_received'])])
```

## View Inheritance

- **Reference**: the documentation related to this topic can be found in Inheritance
- https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_records.html#reference-view-records-inheritance

---

- **Goal**: at the end of this section, the list of available properties linked to a salesperson should be displayed in their user form view
- Instead of modifying existing views in place (by overwriting them), Odoo provides view inheritance where children ‘extension’ views are applied on top of root views
- These extension can both add and remove content from their parent view
- An extension view references its parent using the `inherit_id` field
- Instead of a single view, its `arch` field contains a number of `xpath` elements that select and alter the content of their parent view:

```
<record id="inherited_model_view_form" model="ir.ui.view">
    <field name="name">inherited.model.form.inherit.test</field>
    <field name="model">inherited.model</field>
    <field name="inherit_id" ref="inherited.inherited_model_view_form"/>
    <field name="arch" type="xml">
        <!-- find field description and add the field
             new_field after it -->
        <xpath expr="//field[@name='description']" position="after">
          <field name="new_field"/>
        </xpath>
    </field>
</record>
```

- **expr**
An XPath expression selecting a single element in the parent view. Raises an error if it matches no element or more than one

- **position**
Operation to apply to the matched element:

- **inside**
appends `xpath`’s body to the end of the matched element

- **replace**
replaces the matched element with the `xpath`’s body, replacing any `$0` node occurrence in the new body with the original element

- **before**
inserts the `xpath`’s body as a sibling before the matched element

- **after**
inserts the `xpath`’s body as a sibling after the matched element

- **attributes**
alters the attributes of the matched element using the special `attribute` elements in the `xpath`’s body

---

- When matching a single element, the `position` attribute can be set directly on the element to be found
- Both inheritances below have the same result

```
<xpath expr="//field[@name='description']" position="after">
    <field name="idea_ids" />
</xpath>

<field name="description" position="after">
    <field name="idea_ids" />
</field>
```

---

- **Exercise**: Add fields to the Users view
- Add the `property_ids` field to the `base.view_users_form` in a new notebook page

- **tutorials/estate/views/res_users_views.xml**
```
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>

        <record id="res_users_view_form" model="ir.ui.view">
            <field name="name">res.users.view.form.inherit.estate.property</field>
            <field name="model">res.users</field>
            <field name="inherit_id" ref="base.view_users_form"/>
            <field name="arch" type="xml">
                <xpath expr="//page[@name='preferences']" position="after">
                    <page name="estate_properties" string="Real Estate Properties">
                        <field name="property_ids"/>
                    </page>
                </xpath>
            </field>
        </record>

    </data>
</odoo>
```

