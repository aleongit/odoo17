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
```



