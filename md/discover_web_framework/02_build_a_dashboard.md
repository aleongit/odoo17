# Chapter 2: Build a dashboard

https://www.odoo.com/documentation/17.0/developer/tutorials/discover_js_framework/02_build_a_dashboard.html

The first part of this tutorial introduced you to most of Owl ideas. It is now time to learn about the Odoo JavaScript framework in its entirety, as used by the web client

![Screenshot](odoo_javascript_framework.png)

To get started, you need a running Odoo server and a development environment setup. Before getting into the exercises, make sure you have followed all the steps described in this tutorial introduction. For this chapter, we will start from the empty dashboard provided by the `awesome_dashboard` addon. We will progressively add features to it, using the Odoo JavaScript framework.

- **Solutions**
- https://github.com/odoo/tutorials/commits/17.0-discover-js-framework-solutions/awesome_dashboard


## 1. A new Layout

- Most screens in the Odoo web client uses a common layout: a control panel on top, with some buttons, and a main content zone just below. This is done using the **Layout** component, available in `@web/search/layout`

- https://github.com/odoo/odoo/blob/17.0/addons/web/static/src/search/layout.js

---

1. Update the `AwesomeDashboard` component located in `awesome_dashboard/static/src/` to use the **Layout** component. You can use `{controlPanel: {} }` for the `display` props of the **Layout** component.

2. Add a `className` prop to `Layout: className="'o_dashboard h-100'"`

3. Add a `dashboard.scss` file in which you set the background-color of `.o_dashboard` to gray (or your favorite color)

- Open `http://localhost:8069/web`, then open the **Awesome Dashboard** app, and see the result

- You need to activate **awesome_dashboard** module

---

- **tutorials/awesome_dashboard/static/src/dashboard.js**
```
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout };

  setup() {
    this.display = {
      controlPanel: {},
    };
  }
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboard", AwesomeDashboard);
```

- **tutorials/awesome_dashboard/static/src/dashboard.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">

    <t t-name="awesome_dashboard.AwesomeDashboard">
        <Layout display="display" className="'o_dashboard h-100'">
            <t t-set-slot="layout-buttons">
                 Hello dashboard
            </t>
             some content
        </Layout>
    </t>

</templates>
```

- **tutorials/awesome_dashboard/static/src/dashboard.scss**
```
.o_dashboard {
  background-color: lightgrey;
}
```

---

- 📄 **See also**
- Example: use of Layout in client action and template
- https://github.com/odoo/odoo/blob/17.0/addons/web/static/src/webclient/actions/reports/report_action.js
- https://github.com/odoo/odoo/blob/17.0/addons/web/static/src/webclient/actions/reports/report_action.xml
- Example: use of Layout in kanban view
- https://github.com/odoo/odoo/blob/17.0/addons/web/static/src/views/kanban/kanban_controller.xml

