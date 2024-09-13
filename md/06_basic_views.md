# Chapter 6: Basic Views

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/06_basicviews.html

- We have seen in the previous chapter that Odoo is able to generate default views for a given model
- In practice, the default view is **never** acceptable for a business application. Instead, we should at least organize the various fields in a logical manner

- Views are defined in XML files with actions and menus. They are instances of the `ir.ui.view model`

In our real estate module, we need to organize the fields in a logical way:

- in the list (tree) view, we want to display more than just the name
- in the form view, the fields should be grouped
- in the search view, we must be able to search on more than just the name. Specifically, we want a filter for the ‘Available’ properties and a shortcut to group by postcode


## List

- https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_architectures.html#reference-view-architectures-list

- List views, also called tree views, display records in a tabular form.
- Their root element is `<tree>`. The most basic version of this view simply lists all the fields to display in the table (where each field is a column):

```
<tree string="Tests">
    <field name="name"/>
    <field name="last_seen"/>
</tree>
```

## Add list in Estate Property Model

- **tutorials/estate/views/estate_property_views.xml**
```
<?xml version="1.0"?>
<odoo>

    <!-- action -->
    <record id="estate.property_action" model="ir.actions.act_window">
        <field name="name">Properties</field>
        <field name="res_model">estate.property</field>
        <field name="view_mode">tree,form</field>
    </record>

    <!-- list -->
    <record id="estate.property_list" model="ir.ui.view">
        <field name="name">Property List</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name" string="Title" />
                <field name="postcode"/>
                <field name="bedrooms"/>
                <field name="living_area" string="Living Area (sqm)"/>
                <field name="expected_price"/>
                <field name="selling_price"/>
                <field name="date_availability" string="Available From"/>
            </tree>
        </field>
    </record>

</odoo>
```