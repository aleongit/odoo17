# Chapter 14: A Brief History Of QWeb

https://www.odoo.com/documentation/17.0/developer/tutorials/server_framework_101/14_qwebintro.html

So far the interface design of our real estate module has been rather limited. Building a list view is straightforward since only the list of fields is necessary. The same holds true for the form view: despite the use of a few tags such as `<group>` or `<page>`, there is very little to do in terms of design.

However, if we want to give a unique look to our application, it is necessary to go a step further and be able to design new views. Moreover, other features such as PDF reports or website pages need another tool to be created with more flexibility: a *templating engine*.

You might already be familiar with existing engines such as *Jinja* (Python), *ERB* (Ruby) or *Twig* (PHP). Odoo comes with its own built-in engine: **QWeb Templates**. QWeb is the primary templating engine used by Odoo. It is an XML templating engine and used mostly to generate HTML fragments and pages.

- **QWeb Templates**
https://www.odoo.com/documentation/17.0/developer/reference/frontend/qweb.html#reference-qweb

You probably already have come across the *kanban board* in Odoo where the records are displayed in a card-like structure. We will build such a view for our real estate module.


## Concrete Example: A Kanban View

- **Reference**: the documentation related to this topic can be found in *Kanban*
- https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_architectures.html#reference-view-architectures-kanban

- **Goal**: at the end of this section a Kanban view of the properties should be created

In our estate application, we would like to add a *Kanban* view to display our properties. Kanban views are a standard Odoo view (like the form and list views), but their structure is much more flexible. In fact, the structure of each card is a mix of form elements (including basic HTML) and QWeb. The definition of a Kanban view is similar to the definition of the list and form views, except that their root element is `<kanban>`. In its simplest form, a Kanban view looks like:
```
<kanban>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_global_click">
                <field name="name"/>
            </div>
        </t>
    </templates>
</kanban>
```

Let’s break down this example:

- `<templates>`: defines a list of QWeb Templates templates. Kanban views must define at least one root template kanban-box, which will be rendered once for each record
- `<t t-name="kanban-box">`: `<t>` is a placeholder element for QWeb directives. In this case, it is used to set the name of the template to kanban-box
- `<div class="oe_kanban_global_click">`: the oe_kanban_global_click makes the `<div>` clickable to open the record
- `<field name="name"/>`: this will add the name field to the view

---

- **Exercise**: Make a minimal kanban view
- Using the simple example provided, create a minimal *Kanban* view for the properties
- The only field to display is the `name`.
- *Tip*: you must add kanban in the `view_mode` of the corresponding `ir.actions.act_window`

---

- **tutorials/estate/views/estate_property_views.xml**
```
...
<record id="estate.property_kanban" model="ir.ui.view">
    <field name="name">estate.property.kanban</field>
    <field name="model">estate.property</field>
    <field name="arch" type="xml">
        <kanban>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_global_click">
                        <field name="name"/>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
...
```

- **tutorials/estate/views/estate_actions.xml**
```
<?xml version="1.0"?>
<odoo>
    <record id="estate.property_action" model="ir.actions.act_window">
        <field name="name">Properties</field>
        <field name="res_model">estate.property</field>
        <field name="view_mode">tree,form,kanban</field>
        <field name="context">{'search_default_available': True }</field>
    </record>
...
</odoo>
```

- Once the Kanban view is working, we can start improving it. If we want to display an element conditionally, we can use the `t-if` directive
- **Conditionals**
- https://www.odoo.com/documentation/17.0/developer/reference/frontend/qweb.html#reference-qweb-conditionals

```
<kanban>
    <field name="state"/>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_global_click">
                <field name="name"/>
                <div t-if="record.state.raw_value == 'new'">
                    This is new!
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

We added a few things:

- `t-if`: the `<div>` element is rendered if the condition is true
- `record`: an object with all the requested fields as its attributes Each field has two attributes `value` and `raw_value`
- The former is formatted according to current user parameters and the latter is the direct value from a `read()`

---

- **Exercise**: Improve the Kanban view
- Add the following fields to the Kanban view: *expected price*, *best price*, *selling price* and *tags*
- *Pay attention*: the best price is only displayed when an offer is *received*, while the selling price is only displayed when an offer is *accepted*

---

- **tutorials/estate/views/estate_property_views.xml**
```
<record id="estate.property_kanban" model="ir.ui.view">
    <field name="name">estate.property.kanban</field>
    <field name="model">estate.property</field>
    <field name="arch" type="xml">
        <kanban>
            <!-- list of used fields -->
            <field name="name"/>
            <field name="state"/>
            <field name="expected_price"/>
            <field name="best_price"/>
            <field name="selling_price"/>
            <field name="tag_ids"/>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_global_click">
                        <strong class="o_kanban_record_title">
                            <field name="name"/>
                        </strong>
                        <div class="row">
                            <div class="col-8">
                                <strong>Expected Price:</strong>
                            </div>
                            <div class="col-4 text-end">
                                <field name="expected_price"/>
                            </div>
                        </div>
                        <div t-if="record.state.raw_value == 'offer_received'">
                            <div class="row">
                                <div class="col-8">
                                    <strong>Best Price:</strong>
                                </div>
                                <div class="col-4 text-end">
                                    <field name="best_price"/>
                                </div>
                            </div>
                        </div>
                        <div t-if="record.state.raw_value == 'offer_accepted'">
                            <div class="row">
                                <div class="col-8">
                                    <strong>Selling Price:</strong>
                                </div>
                                <div class="col-4 text-end">
                                    <field name="selling_price"/>
                                </div>
                            </div>
                        </div>
                        <field name="tag_ids"/>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

- Let’s give the final touch to our view: the properties must be *grouped* by *type* by default. You might want to have a look at the various options described in *Kanban*
- https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_architectures.html#reference-view-architectures-kanban

- **Exercise**: Add default grouping
- Use the appropriate attribute to group the properties by type by default. You must also prevent drag and drop.

---

- **tutorials/estate/views/estate_property_views.xml**
```
...
<kanban default_group_by="property_type_id" records_draggable="False">
...
```

Kanban views are a typical example of how it is always a good idea to start from an existing view and fine tune it instead of starting from scratch. There are many options and classes available, so… read and learn!