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


## Form

- https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_architectures.html#reference-view-architectures-form

- Forms are used to create and edit single records

- Their root element is `<form>`. They are composed of high-level structure elements (groups and notebooks) and interactive elements (buttons and fields):

```
<form string="Test">
    <sheet>
        <group>
            <group>
                <field name="name"/>
            </group>
            <group>
                <field name="last_seen"/>
            </group>
        </group>
        <notebook>
            <page string="Description">
                <field name="description"/>
            </page>
        </notebook>
    </sheet>
</form>
```

- **group**: define columns layout
- **sheet**: make the layout responsive
- **notebook** & **page**: add tabbed sections
- https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_architectures.html#structural-components

- It is possible to use regular HTML tags such as **div** and **h1** as well as the the class attribute (Odoo provides some built-in classes) to fine-tune the look

- In order to avoid relaunching the server every time you do a modification to the view, it can be convenient to use the `--dev xml` parameter when launching the server:
- `python3 odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate --dev xml`

## Add form in Estate Property Model

- **tutorials/estate/views/estate_property_views.xml**
```
<!-- form -->
    <record id="estate.property_form" model="ir.ui.view">
        <field name="name">Property</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <form string="Test">
                <sheet>
                    <h1>
                        <field name="name"/>
                    </h1>
                    <group>
                        <group>
                            <field name="postcode"/>
                            <field name="date_availability" string="Available From"/>
                        </group>
                        <group>
                            <field name="expected_price"/>
                            <field name="selling_price"/>
                        </group>
                    </group>

                    <notebook>
                        <page string="Description">
                            <group>
                                <field name="description"/>
                                <field name="bedrooms"/>
                                <field name="living_area" string="Living Area (sqm)"/>
                                <field name="facades"/>
                                <field name="garage"/>
                                <field name="garden"/>
                                <field name="garden_area" string="Garden Area (sqm)"/>
                                <field name="garden_orientation"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
```


## Search

- https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_architectures.html#reference-view-architectures-search

- Search views are slightly different from the list and form views since they don’t display content. 
- Although they apply to a specific model, they are used to filter other views’ content (generally aggregated views such as List). Beyond the difference in use case, they are defined the same way.

- Their root element is `<search>`
- The most basic version of this view simply lists all the fields for which a shortcut is desired:
```
<search string="Tests">
    <field name="name"/>
    <field name="last_seen"/>
</search>
```

- The default search view generated by Odoo provides a shortcut to filter by **name**. 
- It is very common to add the fields which the user is likely to filter on in a customized search view.

## Add search in Estate Property Model

- **tutorials/estate/views/estate_property_views.xml**
```
    <!-- search -->
    <record id="estate.property_search" model="ir.ui.view">
        <field name="name">estate.property.search</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <search string="Busca...">
                <field name="name" string="Title" />
                <field name="postcode"/>
                <field name="expected_price"/>
                <field name="bedrooms"/>
                <field name="living_area" string="Living Area (sqm)"/>
                <field name="facades"/>
            </search>
        </field>
    </record>
```

- Search views can also contain `<filter>` elements, which act as toggles for predefined searches. 

Filters must have one of the following attributes:

- **domain**: adds the given domain to the current search
- **context**: adds some context to the current search; uses the key `group_by` to group results on the given field name

## Domains

- https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html#reference-orm-domains

- In Odoo, a *domain* encodes conditions on records: a *domain* is a list of criteria used to select a subset of a model’s records. Each criterion is a triplet with a *field name*, an *operator* and a *value*. A record satisfies a criterion if the specified field meets the condition of the operator applied to the value

- For instance, when used on the Product model the following domain selects all services with a unit price greater than 1000:
```
[('product_type', '=', 'service'), ('unit_price', '>', 1000)]
```

- By default criteria are combined with an implicit `AND`, meaning every criterion needs to be satisfied for a record to match a domain
- The logical operators `&` (AND), `|` (OR) and `!` (NOT) can be used to explicitly combine criteria
- They are used in prefix position (the operator is inserted before its arguments rather than between)
- For instance, to select products ‘which are services OR have a unit price which is NOT between 1000 and 2000’:
```
['|',
    ('product_type', '=', 'service'),
    '!', '&',
        ('unit_price', '>=', 1000),
        ('unit_price', '<', 2000)]
```

- ⚠️ XML does not allow `<` and `&` to be used inside XML elements
- To avoid parsing errors, entity references should be used: `&lt;` for `<` and `&amp;` for `&`
- Other entity references (`&gt;`, `&apos;` & `&quot;`) are optional
```
<filter name="negative" domain="[('test_val', '&lt;', 0)]"/>
```

## Add filter and Group By

- **tutorials/estate/views/estate_property_views.xml**
```
    <!-- search -->
    <record id="estate.property_search" model="ir.ui.view">
        <field name="name">estate.property.search</field>
        <field name="model">estate.property</field>
        <field name="arch" type="xml">
            <search string="Busca...">
                <field name="name" string="Title" />
                <field name="postcode"/>
                <field name="expected_price"/>
                <field name="bedrooms"/>
                <field name="living_area" string="Living Area (sqm)"/>
                <field name="facades"/>
                <!-- filter domain -->
                <filter string="Available" name="state" domain="['|', ('state', '=', 'new'), ('state', '=', 'offer_received')]"/>
                <!-- group by -->
                <filter name="postcode" context="{'group_by':'postcode'}"/>
            </search>
        </field>
    </record>
```
