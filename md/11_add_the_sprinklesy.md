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

### View

- Ordering is possible at the model level
- This has the advantage of a consistent order everywhere a list of records is retrieved
- However, it is also possible to define a specific order directly in a view thanks to the `default_order` attribute


### Manual

- Both model and view ordering allow flexibility when sorting records, but there is still one case we need to cover: the manual ordering
- A user may want to sort records depending on the business logic
- For example, in our real estate module we would like to sort the property types manually
- It is indeed useful to have the most used types appear at the top of the list
- If our real estate agency mainly sells houses, it is more convenient to have *House* appear before *Apartment*
- To do so, a `sequence` field is used in combination with the `handle` widget
- Obviously the `sequence` field must be the first field in the `_order` attribute


- **Exercise**: Add manual ordering
- Add the following field in `estate.property.type`:
- `Sequence` (Integer)
- Add the sequence to the `estate.property.type` list view with the correct widget


- **tutorials/estate/models/estate_property_type.py**
```
class EstatePropertyType(models.Model):
    _name = "estate.property.type"
...
    sequence = fields.Integer('Sequence', default=1, help="Used to order types")
...
```

- **tutorials/estate/views/estate_property_type_views.xml**
```
...
    <record id="estate.property_type_list" model="ir.ui.view">
...
            <tree>
                <field name="sequence" widget="handle"/>
                <field name="name" string="Type" />
            </tree>
...
```

## Attributes and options

- It would be prohibitive to detail all the available features which allow fine tuning of the look of a view


### Form

- **Goal**: at the end of this section, the property form view will have:
- Conditional display of buttons and fields
- Tag colors

- In our real estate module, we want to modify the behavior of some fields
- For example, we don’t want to be able to create or edit a property type from the form view
- Instead we expect the types to be handled in their appropriate menu
- We also want to give tags a color. In order to add these behavior customizations, we can add the **options** attribute to several field widgets

- **Exercise**: Add widget options
- Add the appropriate option to the *property_type_id* field to prevent the creation and the editing of a property type from the property form view
- Have a look at the Many2one widget documentation for more info
- Add the following field:
- *Color* (Integer) in *estate.property.tag* model
- Then add the appropriate option to the *tag_ids* field to add a color picker on the tags
- Have a look at the *FieldMany2ManyTags* widget documentation for more info
- https://www.odoo.com/documentation/17.0/developer/reference/frontend/javascript_reference.html#reference-js-widgets


- **tutorials/estate/views/estate_property_views.xml**
```
<field name="tag_ids" widget="many2many_tags" options="{'color_field': 'color'}"/>
...
<field name="property_type_id" options="{'no_create': true, 'no_open': true}"/>
```


- **tutorials/estate/models/estate_property_tag.py**
```
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
...
    color = fields.Integer(string='Color')
```

- In *Chapter 5: Finally, Some UI To Play With*, we saw that reserved fields were used for specific behaviors
- For example, the active field is used to automatically filter out inactive records
- We added the state as a reserved field as well
- It’s now time to use it! A state field can be used in combination with an invisible attribute in the view to display buttons conditionally


- **Exercise**: Add conditional display of buttons
- Use the *invisible* attribute to display the header buttons conditionally as depicted in this section’s Goal (notice how the ‘Sold’ and ‘Cancel’ buttons change when the state is modified).
- *Tip*: do not hesitate to search for invisible= in the Odoo XML files for some examples

- **tutorials/estate/views/estate_property_views.xml**
```
<button name="action_set_sold" type="object" string="Sold" 
    invisible="state in ('sold', 'canceled')"/>

<button name="action_set_canceled" type="object" string="Canceled" 
    invisible="state in ('sold', 'canceled')"/>
```

- More generally, it is possible to make a field *invisible*, *readonly* or *required* based on the value of other fields
- Note that *invisible* can also be applied to other elements of the view such as *button* or *group*

- *invisible*, *readonly* and *required* can have any Python expression as value
- The expression gives the condition in which the property applies. For example:
```
<form>
    <field name="description" invisible="not is_partner"/>
    <field name="is_partner" invisible="True"/>
</form>
```

- This means that the *description* field is *invisible* when *is_partner* is *False*
- It is important to note that a field used in *invisible* **must** be present in the view
- If it should not be displayed to the user, we can use the *invisible* attribute to hide it

- **Exercise**: Use invisible
- Make the garden area and orientation invisible in the *estate.property* form view when there is no garden
- Make the ‘Accept’ and ‘Refuse’ buttons invisible once the offer state is set
- Do not allow adding an offer when the property state is ‘Offer Accepted’, ‘Sold’ or ‘Canceled’. To do this use the *readonly* attribute
- ⚠️ **Warning**
- Using a (conditional) *readonly* attribute in the view can be useful to prevent data entry errors, but keep in mind that it doesn’t provide any level of security! There is no check done server-side, therefore it’s always possible to write on the field through a RPC call

- **tutorials/estate/views/estate_property_views.xml**
```
<page string="Description">
    <group>
...
        <field name="garden"/>
        <field name="garden_area" string="Garden Area (sqm)" invisible="not garden"/>
        <field name="garden_orientation" invisible="not garden"/>
...
    </group>
</page>
...
<page string="Offers">
    <field name="offer_ids" 
        readonly="state in ('offer_accepted', 'sold', 'canceled')"/>
</page>
```

- **tutorials/estate/views/estate_property_offer_views.xml**
```
<tree>
...
    <button name="action_accept_offer" title = "accept" type="object" icon="fa-check" invisible="state"/>
    <button name="action_refuse_offer" title = "refuse" type="object" icon="fa-times" invisible="state"/>
...
</tree>
```

### List

- **Goal**: at the end of this section, the property and offer list views should have color decorations
- Additionally, offers and tags will be editable directly in the list, and the availability date will be hidden by default

---

- When the model only has a few fields, it can be useful to edit records directly through the list view and not have to open the form view
- In the real estate example, there is no need to open a form view to add an offer or create a new tag
- This can be achieved thanks to the `editable` attribute

---

- **Exercise**: Make list views editable
- Make the `estate.property.offer` and `estate.property.tag` list views editable

- **tutorials/estate/views/estate_property_offer_views.xml**
```
...
<record id="estate.property_offer_list" model="ir.ui.view">
    <field name="name">Property Offer List</field>
    <field name="model">estate.property.offer</field>
    <field name="arch" type="xml">
        <tree editable="top">
...
```

- On the other hand, when a model has a lot of fields it can be tempting to add too many fields in the list view and make it unclear
- An alternative method is to add the fields, but make them optionally hidden
- This can be achieved thanks to the `optional` attribute

---

- **Exercise**: Make a field optional
- Make the field `date_availability` on the `estate.property` list view optional and hidden by default

- **tutorials/estate/views/estate_property_views.xml**
```
<record id="estate.property_list" model="ir.ui.view">
    <field name="name">Property List</field>
    <field name="model">estate.property</field>
    <field name="arch" type="xml">
        <tree>
...
            <field name="date_availability" string="Available From" optional="hide"/>
...
```

- Finally, color codes are useful to visually emphasize records
- For example, in the real estate module we would like to display refused offers in red and accepted offers in green
- This can be achieved thanks to the `decoration-{$name}` attribute (see Fields for a complete list):
- https://www.odoo.com/documentation/17.0/developer/reference/frontend/javascript_reference.html#reference-js-widgets


```
<tree decoration-success="is_partner==True">
    <field name="name"/>
    <field name="is_partner" invisible="1"/>
</tree>
```
- The records where `is_partner` is `True` will be displayed in green

---

- **Exercise**: Add some decorations
- On the `estate.property` list view:
- Properties with an offer received are green
- Properties with an offer accepted are green and bold
- Properties sold are muted

- **tutorials/estate/views/estate_property_views.xml**
```
<record id="estate.property_list" model="ir.ui.view">
    <field name="name">Property List</field>
    <field name="model">estate.property</field>
    <field name="arch" type="xml">
        <tree 
            decoration-success="state in ('offer_received','offer_accepted')"
            decoration-bf="state == 'offer_accepted'"
            decoration-muted="state == 'sold'"
        >
```

- On the `estate.property.offer` list view:
- Refused offers are red
- Accepted offers are green
- The state should not be visible anymore

- **Tips**:
- Keep in mind that all fields used in attributes must be in the view!
- If you want to test the color of the “Offer Received” and “Offer Accepted” states, add the field in the form view and change it manually (we’ll implement the business logic for this later)

- **tutorials/estate/views/estate_property_offer_views.xml**
```
<record id="estate.property_offer_list" model="ir.ui.view">
    <field name="name">Property Offer List</field>
    <field name="model">estate.property.offer</field>
    <field name="arch" type="xml">
        <tree editable="top" 
            decoration-danger="state == 'refused'"
            decoration-success="state == 'accepted'">
...
            <field name="state" invisible="1" optional="hide" />
...
```