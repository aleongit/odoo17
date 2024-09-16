# Chapter 8: Computed Fields And Onchanges

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/08_compute_onchange.html

The relations between models are a key component of any Odoo module. They are necessary for the modelization of any business case. However, we may want links between the fields within a given model. Sometimes the value of one field is determined from the values of other fields and other times we want to help the user with data entry

These cases are supported by the concepts of _computed fields_ and _onchanges_. Although this chapter is not technically complex, the semantics of both concepts is very important. This is also the first time we will write Python logic. Until now we haven’t written anything other than class definitions and field declarations

## Computed Fields

- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#reference-fields-compute

Goal: at the end of this section:

- In the property model, the total area and the best offer should be computed
- In the property offer model, the validity date should be computed and can be updated

---

- In our real estate module, we have defined the living area as well as the garden area. It is then natural to define the total area as the sum of both fields. We will use the concept of a computed field for this, i.e. the value of a given field will be computed from the value of other fields

- So far fields have been stored directly in and retrieved directly from the database. Fields can also be computed. In this case, the field’s value is not retrieved from the database but computed on-the-fly by calling a method of the model

- To create a computed field, create a field and set its attribute `compute` to the name of a method. The computation method should set the value of the computed field for every record in self

- By convention, `compute` methods are private, meaning that they cannot be called from the presentation tier, only from the business tier (see Chapter 1: Architecture Overview). Private methods have a name starting with an underscore `_`

## Dependencies

- The value of a computed field usually depends on the values of other fields in the computed record. The ORM expects the developer to specify those dependencies on the compute method with the decorator `depends()`. The given dependencies are used by the ORM to trigger the recomputation of the field whenever some of its dependencies have been modified:

```
from odoo import api, fields, models

class TestComputed(models.Model):
    _name = "test.computed"

    total = fields.Float(compute="_compute_total")
    amount = fields.Float()

    @api.depends("amount")
    def _compute_total(self):
        for record in self:
            record.total = 2.0 * record.amount
```

- `self` is a collection

- The object `self` is a **recordset**, i.e. an ordered collection of records. It supports the standard Python operations on collections, e.g. `len(self)` and `iter(self)`, plus extra set operations such as `recs1` | `recs2`

Iterating over `self` gives the records one by one, where each record is itself a collection of size **1**. You can access/assign fields on single records by using the dot notation, e.g. `record.name`

## Add a computed field

- Add the _total_area_ field to _estate.property_. It is defined as the sum of the living_area and the garden_area
- Add the field in the form view

---

- **tutorials/estate/models/estate_property.py**

```
# computed fields
total_area = fields.Float(compute="_compute_total_area")

@api.depends('living_area', 'garden_area')
def _compute_total_area(self):
    for record in self:
        record.total_area = record.living_area + record.garden_area
```

- **tutorials/estate/views/estate_property_views.xml**

```
<!-- pag description -->
<page string="Description">
    <group>
...
        <field name="living_area" string="Living Area (sqm)"/>
        <field name="garden_area" string="Garden Area (sqm)"/>
        <field name="total_area" string="Total Area (sqm)"/>
    </group>
</page>
```

- For relational fields it’s possible to use paths through a field as a dependency:

```
description = fields.Char(compute="_compute_description")
partner_id = fields.Many2one("res.partner")

@api.depends("partner_id.name")
def _compute_description(self):
    for record in self:
        record.description = "Test for partner %s" % record.partner_id.name
```

- The example is given with a **Many2one**, but it is valid for _Many2many_ or a _One2many_

## Compute the best offer

- Add the _best_price_ field to _estate.property_. It is defined as the highest (i.e. maximum) of the offers’ price
- Add the field to the form view
- Tip: you might want to try using the `mapped()` method
- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.models.Model.mapped

- **tutorials/estate/models/estate_property.py**

```
best_price = fields.Float(compute="_compute_best_price")

@api.depends('offer_ids')
def _compute_best_price(self):
    for record in self:
        if record.offer_ids:
            record.best_price = max(record.offer_ids.mapped('price'))
        else:
            record.best_price = 0
```
