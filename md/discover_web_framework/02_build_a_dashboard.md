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


## Theory: Services

In practice, every component (except the root component) may be destroyed at any time and replaced (or not) with another component. This means that each component internal state is not persistent. This is fine in many cases, but there certainly are situations where we want to keep some data around. For example, all Discuss messages should not be reloaded every time we display a channel.

Also, it may happen that we need to write some code that is not a component. Maybe something that process all barcodes, or that manages the user configuration (context, etc.).

The Odoo framework defines the idea of a **service**, which is a persistent piece of code that exports state and/or functions. Each service can depend on other services, and components can import a service

- https://www.odoo.com/documentation/17.0/developer/reference/frontend/services.html#frontend-services

The following example registers a simple service that displays a notification every 5 seconds:
```
import { registry } from "@web/core/registry";

const myService = {
    dependencies: ["notification"],
    start(env, { notification }) {
        let counter = 1;
        setInterval(() => {
            notification.add(`Tick Tock ${counter++}`);
        }, 5000);
    },
};

registry.category("services").add("myService", myService);
```

Services can be accessed by any component. Imagine that we have a service to maintain some shared state:
```
import { registry } from "@web/core/registry";

const sharedStateService = {
    start(env) {
        let state = {};
        return {
            getValue(key) {
                return state[key];
            },
            setValue(key, value) {
                state[key] = value;
            },
        };
    },
};

registry.category("services").add("shared_state", sharedStateService);
```

Then, any component can do this:
```
import { useService } from "@web/core/utils/hooks";

setup() {
   this.sharedState = useService("shared_state");
   const value = this.sharedState.getValue("somekey");
   // do something with value
}
```

## 2. Add some buttons for quick navigation

One important service provided by Odoo is the `action` service: it can execute all kind of standard actions defined by Odoo. For example, here is how one component could execute an *action* by its *xml* id:
```
import { useService } from "@web/core/utils/hooks";
...
setup() {
      this.action = useService("action");
}
openSettings() {
      this.action.doAction("base_setup.action_general_configuration");
}
...
```

Let us now add two buttons to our control panel:

1. A button `Customers`, which opens a kanban view with all customers (this action already exists, so you should use its xml id).
- https://github.com/odoo/odoo/blob/1f4e583ba20a01f4c44b0a4ada42c4d3bb074273/odoo/addons/base/views/res_partner_views.xml#L510

2. A button `Leads`, which opens a dynamic action on the `crm.lead` model with a list and a form view. Follow the example of this use of the action service.
- https://github.com/odoo/odoo/blob/ef424a9dc22a5abbe7b0a6eff61cf113826f04c0/addons/account/static/src/components/journal_dashboard_activity/journal_dashboard_activity.js#L28-L35

---

- **tutorials/awesome_dashboard/static/src/dashboard.js**
```
/** @odoo-module **/
...
import { useService } from "@web/core/utils/hooks";

class AwesomeDashboard extends Component {
...

  setup() {
    this.action = useService("action");
    this.display = {
      controlPanel: {},
    };
  }

  openCustomerView() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads() {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: "All leads",
      res_model: "crm.lead",
      views: [
        [false, "list"],
        [false, "form"],
      ],
    });
  }
}
...
```

- **tutorials/awesome_dashboard/static/src/dashboard.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">

    <t t-name="awesome_dashboard.AwesomeDashboard">
        <Layout display="display" className="'o_dashboard h-100'">
            <t t-set-slot="layout-buttons">
                <button class="btn btn-primary" 
                    t-on-click="openCustomerView">Customers</button>
                <button class="btn btn-primary" 
                    t-on-click="openLeads">Leads</button>
            </t>
             some content
        </Layout>
    </t>

</templates>
```

- 📄 **See also**
- Code: action service
- https://github.com/odoo/odoo/blob/17.0/addons/web/static/src/webclient/actions/action_service.js


## 3. Add a dashboard item