# Chapter 9: Ready For Some Action?

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/09_actions.html


So far we have mostly built our module by declaring fields and views. We just introduced business logic in the previous chapter thanks to computed fields and onchanges. In any real business scenario, we would want to link some business logic to action buttons. In our real estate example, we would like to be able to:

- cancel or set a property as sold
- accept or refuse an offer

One could argue that we can already do these things by changing the state manually, but this is not really convenient. Moreover, we want to add some extra processing: when an offer is accepted we want to set the selling price and the buyer for the property

## Object Type

- **Actions**
-  https://www.odoo.com/documentation/17.0/developer/reference/backend/actions.html

- **Error management**
- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#reference-exceptions

In our real estate module, we want to link business logic with some buttons. The most common way to do this is to:
- Add a button in the view, for example in the header of the view:
```
<form>
    <header>
        <button name="action_do_something" type="object" string="Do Something"/>
    </header>
    <sheet>
        <field name="name"/>
    </sheet>
</form>
```

- and link this button to business logic:
```
from odoo import fields, models

class TestAction(models.Model):
    _name = "test.action"

    name = fields.Char()

    def action_do_something(self):
        for record in self:
            record.name = "Something"
        return True
```

- By assigning `type="object"` to our *button*, the Odoo framework will execute a Python method with `name="action_do_something"` on the given model

- The first important detail to note is that our method name isn’t prefixed with an underscore (`_`). This makes our method a public method, which can be called directly from the Odoo interface (through an RPC call). Until now, all methods we created (compute, onchange) were called internally, so we used private methods prefixed by an underscore. You should always define your methods as **private** unless they need to be called from the user interface

- Also note that we loop on `self`. Always assume that a method can be called on multiple records; it’s better for reusability.

Finally, a public method should always return something so that it can be called through XML-RPC. When in doubt, just `return True`.


## Add actions (Cancel and set a property as sold)

- Add the buttons ‘Cancel’ and ‘Sold’ to the `estate.property` model. A canceled property cannot be set as sold, and a sold property cannot be canceled
- Tip: in order to raise an error, you can use the `UserError` function
- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#reference-exceptions

---

- **tutorials/estate/views/estate_property_views.xml**
```
<header>
    <button name="action_set_sold" type="object" string="Sold"/>
    <button name="action_set_canceled" type="object" string="Canceled"/>
</header>
```

- **tutorials/estate/models/estate_property.py**
```
def action_set_sold(self):
    if self.state != 'canceled':
        self.state = 'sold'
    else:
        raise UserError("Canceled properties cannot be sold!")
    return True

def action_set_canceled(self):
    if self.state != 'sold':
        self.state = 'canceled'
    else:
        raise UserError("Sold properties cannot be canceled!")
    return True
```

- Add the buttons ‘Accept’ and ‘Refuse’ to the `estate.property.offer` model
- When an offer is accepted, set the *buyer* and the *selling price* for the corresponding property
- ⚠️ Pay attention: in real life only one offer can be accepted for a given property!
- **tutorials/estate/models/estate_property_offer.py**
```
# action methods
def action_accept_offer(self):
    if not 'accepted' in self.property_id.offer_ids.mapped('state'):
        self.state = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
    else:
        raise UserError("Only 1 offer can be accepted!")
    return True

def action_refuse_offer(self):
    if self.state == 'accepted':
        self.property_id.selling_price = 0
        self.property_id.buyer_id = None
    self.state = 'refused'
    return True
```

- **tutorials/estate/views/estate_property_offer_views.xml**
```
<!-- tree -->
<record id="estate.property_offer_list" model="ir.ui.view">
    <field name="name">Property Offer List</field>
    <field name="model">estate.property.offer</field>
    <field name="arch" type="xml">
        <tree>
            <field name="price" />
            <field name="partner_id" />
            <field name="validity" />
            <field name="date_deadline" />
                <button name="action_accept_offer" title = "accept" type="object" icon="fa-check"/>
                <button name="action_refuse_offer" title = "refuse" type="object" icon="fa-times"/>
            <field name="state" />
        </tree>
    </field>
</record>
```

## Action Type

- In *Chapter 5: Finally, Some UI To Play With*, we created an action that was linked to a menu. You may be wondering if it is possible to link an action to a button. Good news, it is! One way to do it is:
```
<button type="action" name="%(test.test_model_action)d" string="My Action"/>
```

- We use `type="action"` and we refer to the *external identifier* in the `name`