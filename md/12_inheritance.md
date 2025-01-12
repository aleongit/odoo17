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