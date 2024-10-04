# Chapter 10: Constraints

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/10_constraints.html

The previous chapter introduced the ability to add some business logic to our model. We can now link buttons to business code, but how can we prevent users from entering incorrect data? For example, in our real estate module nothing prevents users from setting a negative expected price

Odoo provides two ways to set up automatically verified invariants: 
**Python constraints** and **SQL constraints**
- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#odoo.api.constrains


## SQL

- Reference: the documentation related to this topic can be found in Models and in the PostgreSQL’s documentation

- **SQL constraints** are defined through the model attribute `_sql_constraints`. This attribute is assigned a list of triples containing strings `(name, sql_definition, message)`, where `name` is a valid SQL constraint name, `sql_definition` is a **table_constraint** expression and message is the error message
- https://www.postgresql.org/docs/12/ddl-constraints.html

```
_sql_constraints = [
        ('check_percentage', 'CHECK(percentage >= 0 AND percentage <= 100)',
         'The percentage of an analytic distribution should be between 0 and 100.')
    ]
```

## Add SQL constraints

Add the following constraints to their corresponding models:
- A property expected price must be strictly positive
- A property selling price must be positive
- An offer price must be strictly positive
- A property tag name and property type name must be unique
- Tip: search for the `unique` keyword in the Odoo codebase for examples of unique names
- Restart the server with the -u estate option to see the result. Note that you might have data that prevents a SQL constraint from being set. An error message similar to the following might pop up:
```
ERROR rd-demo odoo.schema: Table 'estate_property_offer': unable to add constraint 'estate_property_offer_check_price' as CHECK(price > 0)
```
- For example, if some offers have a price of zero, then the constraint can’t be applied. You can delete the problematic data in order to apply the new constraints

-**tutorials/estate/models/estate_property.py**
```
# sql constraints
_sql_constraints = [
    ('check_property_expected_price', 'CHECK(expected_price > 0)',
        'A property expected price must be strictly positive'),
    ('check_property_selling_price', 'CHECK(selling_price >= 0)',
        'A property selling price must be positive')
]
```

-**tutorials/estate/models/estate_property_offer.py**
```
# sql constraints
_sql_constraints = [
    ('check_property_offer_price', 'CHECK(price > 0)',
        'An offer price must be strictly positive'),
]
```

-**tutorials/estate/models/estate_property_type.py**
```
# sql constraints
_sql_constraints = [
    ('check_property_type_name', 'UNIQUE(name)',
        'A property type name must be unique'),
]
```

-**tutorials/estate/models/estate_property_tag.py**
```
# sql constraints
_sql_constraints = [
    ('check_property_tag_name', 'UNIQUE(name)',
        'A property tag name must be unique'),
]
```