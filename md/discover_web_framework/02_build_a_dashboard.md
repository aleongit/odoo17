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

Let us now improve our content.

1. Create a generic `DashboardItem` component that display its default slot in a nice card layout. It should take an optional `size` number props, that default to `1`. The width should be hardcoded to`(18*size)rem`

2. Add two cards to the dashboard. One with no size, and the other with a size of 2.

- **tutorials/awesome_dashboard/static/src/dashboard_item/dashboard_item.js**
```
/** @odoo-module */
import { Component } from "@odoo/owl";

export class DashboardItem extends Component {
  static template = "awesome_dashboard.DashboardItem";
  static props = {
    slots: {
      type: Object,
      shape: {
        default: Object,
      },
    },
    size: {
      type: Number,
      default: 1,
      optional: true,
    },
  };
}
```

- **tutorials/awesome_dashboard/static/src/dashboard_item/dashboard_item.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_dashboard.DashboardItem">
        <div class="card m-2 border-dark" t-attf-style="width: {{18*props.size}}rem;">
            <div class="card-body">
                <t t-slot="default"/>
            </div>
        </div>
    </t>
</templates>
```

- **tutorials/awesome_dashboard/static/src/dashboard.js**
```
import { DashboardItem } from "./dashboard_item/dashboard_item";
...

class AwesomeDashboard extends Component {
  static components = { Layout, DashboardItem };
...
}

```

- **tutorials/awesome_dashboard/static/src/dashboard.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_dashboard.AwesomeDashboard">
        <Layout display="display" className="'o_dashboard h-100'">
            <t t-set-slot="layout-buttons">
                <button class="btn btn-primary" t-on-click="openCustomerView">Customers</button>
                <button class="btn btn-primary" t-on-click="openLeads">Leads</button>
            </t>
            <div class="d-flex flex-wrap">
                <DashboardItem>
                    some content
                </DashboardItem>
                <DashboardItem size="2">
                    I love milk
                </DashboardItem>
                <DashboardItem>
                    some content
                </DashboardItem>
            </div>
        </Layout>
    </t>
</templates>
```

## 4. Call the server, add some statistics

Let’s improve the dashboard by adding a few dashboard items to display real business data. The `awesome_dashboard` addon provides a `/awesome_dashboard/statistics` route that is meant to return some interesting information.

To call a specific controller, we need to use the **rpc service**. It only exports a single function that perform the request: `rpc(route, params, settings`)`. A basic request could look like this:

- https://www.odoo.com/documentation/17.0/developer/reference/frontend/services.html#frontend-services-rpc

```
setup() {
      this.rpc = useService("rpc");
      onWillStart(async () => {
         const result = await this.rpc("/my/controller", {a: 1, b: 2});
         // ...
      });
}
```

1. Update `Dashboard` so that it uses the `rpc` service
2. Call the statistics route `/awesome_dashboard/statistics` in the `onWillStart` hook.
3. Display a few cards in the dashboard containing:
- Number of new orders this month
- Total amount of new orders this month
- Average amount of t-shirt by order this month
- Number of cancelled orders this month
- Average time for an order to go from ‘new’ to ‘sent’ or ‘cancelled’


- **tutorials/awesome_dashboard/static/src/dashboard.js**
```
import { Component, onWillStart  } from "@odoo/owl";
...

  setup() {
    this.action = useService("action");
    this.rpc = useService("rpc");
    this.display = {
      controlPanel: {},
    };
    
    onWillStart(async () => {
            this.statistics = await this.rpc("/awesome_dashboard/statistics");
        });
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
                <button class="btn btn-primary" t-on-click="openCustomerView">Customers</button>
                <button class="btn btn-primary" t-on-click="openLeads">Leads</button>
            </t>
            <div class="d-flex flex-wrap">
                <DashboardItem>
                    some content
                </DashboardItem>
                <DashboardItem size="2">
                    I love milk
                </DashboardItem>
                <DashboardItem>
                    some content
                </DashboardItem>
                <DashboardItem>
                    Average amount of t-shirt by order this month
                    <div class="fs-1 fw-bold text-success text-center">
                        <t t-esc="statistics.average_quantity"/>
                    </div>
                </DashboardItem>
                <DashboardItem>
                    Average time for an order to go from 'new' to 'sent' or 'cancelled'
                    <div class="fs-1 fw-bold text-success text-center">
                        <t t-esc="statistics.average_time"/>
                    </div>
                </DashboardItem>
                <DashboardItem>
                    Number of new orders this month
                    <div class="fs-1 fw-bold text-success text-center">
                        <t t-esc="statistics.nb_new_orders"/>
                    </div>
                </DashboardItem>
                <DashboardItem>
                    Number of cancelled orders this month
                    <div class="fs-1 fw-bold text-success text-center">
                        <t t-esc="statistics.nb_cancelled_orders"/>
                    </div>
                </DashboardItem>
                <DashboardItem>
                    Total amount of new orders this month
                    <div class="fs-1 fw-bold text-success text-center">
                        <t t-esc="statistics.total_amount"/>
                    </div>
                </DashboardItem>
            </div>
        </Layout>
    </t>
</templates>
```




## 5. Cache network calls, create a service

If you open the **Network** tab of your browser’s dev tools, you will see that the call to `/awesome_dashboard/statistics` is done every time the client action is displayed. This is because the `onWillStart` hook is called each time the `Dashboard` component is mounted. But in this case, we would prefer to do it only the first time, so we actually need to maintain some state outside of the `Dashboard` component. This is a nice use case for a service!

1. Register and import a new `awesome_dashboard.statistics` service.
2. It should provide a function `loadStatistics` that, once called, performs the actual rpc, and always return the same information.
3. Use the *memoize* utility function from `@web/core/utils/functions` that allows caching the statistics.
4. Use this service in the `Dashboard` component.
5. Check that it works as expected.

- https://github.com/odoo/odoo/blob/17.0/addons/web/static/src/core/network/http_service.js
- https://github.com/odoo/odoo/blob/17.0/addons/web/static/src/core/user_service.js


- **tutorials/awesome_dashboard/static/src/statistics_service.js**
```
/** @odoo-module */

import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";

const statisticsService = {
  dependencies: ["rpc"],
  async: ["loadStatistics"],
  start(env, { rpc }) {
    return {
      loadStatistics: memoize(() => rpc("/awesome_dashboard/statistics")),
    };
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
```

- **tutorials/awesome_dashboard/static/src/dashboard.js**
```
  setup() {
    this.action = useService("action");
    // this.rpc = useService("rpc");
    this.statistics = useService("awesome_dashboard.statistics");
    this.display = {
      controlPanel: {},
    };

    onWillStart(async () => {
      // this.statistics = await this.rpc("/awesome_dashboard/statistics");
      this.statistics = await this.statistics.loadStatistics();
    });
  }
```


## 6. Display a pie chart

Everyone likes charts (!), so let us add a pie chart in our dashboard. It will display the proportions of t-shirts sold for each size: S/M/L/XL/XXL.

For this exercise, we will use **Chart.js**. It is the chart library used by the graph view. However, it is not loaded by default, so we will need to either add it to our assets bundle, or lazy load it. Lazy loading is usually better since our users will not have to load the chartjs code every time if they don’t need it.

1. Create a `PieChart` component.
2. In its `onWillStart` method, load chartjs, you can use the `loadJs` function to load `/web/static/lib/Chart/Chart.js`.
3. Use the `PieChart` component in a `DashboardItem` to display a pie chart that shows the quantity for each sold t-shirts in each size (that information is available in the `/statistics` route). Note that you can use the `size` property to make it look larger.
4. The `PieChart` component will need to render a canvas, and draw on it using `chart.js`.
5. Make it work!

- **tutorials/awesome_dashboard/static/src/pie_chart/pie_chart.js**
```
/** @odoo-module */

import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import {
  Component,
  onWillStart,
  useRef,
  onMounted,
  onWillUnmount,
} from "@odoo/owl";

export class PieChart extends Component {
  static template = "awesome_dashboard.PieChart";
  static props = {
    label: String,
    data: Object,
  };

  setup() {
    this.canvasRef = useRef("canvas");
    onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
    onMounted(() => {
      this.renderChart();
    });
    onWillUnmount(() => {
      this.chart.destroy();
    });
  }

  renderChart() {
    const labels = Object.keys(this.props.data);
    const data = Object.values(this.props.data);
    const color = labels.map((_, index) => getColor(index));
    this.chart = new Chart(this.canvasRef.el, {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            label: this.props.label,
            data: data,
            backgroundColor: color,
          },
        ],
      },
    });
  }
}
```

- **tutorials/awesome_dashboard/static/src/pie_chart/pie_chart.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_dashboard.PieChart">
        <div t-att-class="'h-100 ' + props.class" t-ref="root">
            <div class="h-100 position-relative" t-ref="container">
                <canvas t-ref="canvas" />
            </div>
        </div>
    </t>
</templates>
```

- **tutorials/awesome_dashboard/static/src/dashboard.js**
```
...
import { PieChart } from "./pie_chart/pie_chart";
...
class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem, PieChart };
...
```

- **tutorials/awesome_dashboard/static/src/dashboard.xml**
```
...
<DashboardItem size="2">
    Shirt orders by size
    <PieChart data="statistics['orders_by_size']" label="'Shirt orders by size'"/>
</DashboardItem>
...
```


## 7. Real life update

Since we moved the data loading in a cache, it never updates. But let us say that we are looking at fast moving data, so we want to periodically (for example, every 10min) reload fresh data.

This is quite simple to implement, with a `setTimeout` or `setInterval` in the statistics service. However, here is the tricky part: if the dashboard is currently being displayed, it should be updated immediately.

To do that, one can use a `reactive` object: it is just like the proxy returned by `useState`, but not linked to any component. A component can then do a `useState` on it to subscribe to its changes.

1. Update the statistics service to reload data every 10 minutes (to test it, use 10s instead!)
2. Modify it to return a **reactive** object. Reloading data should update the reactive object in place.
3. The `Dashboard` component can now use it with a `useState`

https://github.com/odoo/owl/blob/master/doc/v2/reference/reactivity.md#reactive
https://github.com/odoo/owl/blob/master/doc/v2/reference/reactivity.md

- **tutorials/awesome_dashboard/static/src/statistics_service.js**
```
/** @odoo-module */

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const statisticsService = {
  dependencies: ["rpc"],
  start(env, { rpc }) {
    const statistics = reactive({ isReady: false });

    async function loadData() {
      const updates = await rpc("/awesome_dashboard/statistics");
      Object.assign(statistics, updates, { isReady: true });
    }

    setInterval(loadData, 10 * 60 * 1000);
    loadData();

    return statistics;
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
```


- **tutorials/awesome_dashboard/static/src/dashboard.js**
```
/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
...

class AwesomeDashboard extends Component {
...
  setup() {
    this.statistics = useState(useService("awesome_dashboard.statistics"));
  }
}
...
```

- **tutorials/awesome_dashboard/static/src/dashboard.xml**
```
...
<div class="d-flex flex-wrap" t-if="statistics.isReady">
    <DashboardItem>
        some content
    </DashboardItem>
...
```

## 8. Lazy loading the dashboard

Let us imagine that our dashboard is getting quite big, and is only of interest to some of our users. In that case, it could make sense to lazy load our dashboard, and all related assets, so we only pay the cost of loading the code when we actually want to look at it.

One way to do this is to use `LazyComponent` (from `@web/core/assets`) as an intermediate that will load an asset bundle before displaying our component.

**example_action.js:**
```
export class ExampleComponentLoader extends Component {
    static components = { LazyComponent };
    static template = xml`
        <LazyComponent bundle="'example_module.example_assets'" Component="'ExampleComponent'" />
    `;
}

registry.category("actions").add("example_module.example_action", ExampleComponentLoader);
```

1. Move all dashboard assets into a sub folder `/dashboard` to make it easier to add to a bundle.
2. Create a `awesome_dashboard.dashboard` assets bundle containing all content of the `/dashboard` folder.
3. Modify `dashboard.js` to register itself to the `lazy_components` registry instead of `actions`.
4. In `src/dashboard_action.js`, create an intermediate component that uses `LazyComponent` and register it to the `actions` registry.


- **tutorials/awesome_dashboard/__manifest__.py**
```
{
    'name': "Awesome Dashboard",
...
    'assets': {
        'web.assets_backend': [
            'awesome_dashboard/static/src/**/*',
            ('remove', 'awesome_dashboard/static/src/dashboard/**/*'),
        ],
        'awesome_dashboard.dashboard': [
            'awesome_dashboard/static/src/dashboard/**/*'
        ]
    },
    'license': 'AGPL-3'
}
```

- **tutorials/awesome_dashboard/static/src/dashboard_loader.js**
```
/** @odoo-module */

import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";
import { Component, xml } from "@odoo/owl";

class AwesomeDashboardLoader extends Component {
  static components = { LazyComponent };
  static template = xml`
    <LazyComponent bundle="'awesome_dashboard.dashboard'" Component="'AwesomeDashboard'" props="props"/>
    `;
}

registry
  .category("actions")
  .add("awesome_dashboard.dashboard", AwesomeDashboardLoader);

```


## 9. Making our dashboard generic

So far, we have a nice working dashboard. But it is currently hardcoded in the dashboard template. What if we want to customize our dashboard? Maybe some users have different needs and want to see other data.

So, the next step is to make our dashboard generic: instead of hard-coding its content in the template, it can just iterate over a list of dashboard items. But then, many questions come up: how to represent a dashboard item, how to register it, what data should it receive, and so on. There are many different ways to design such a system, with different trade-offs.

For this tutorial, we will say that a dashboard item is an object with the following structure:

```
const item = {
   id: "average_quantity",
   description: "Average amount of t-shirt",
   Component: StandardItem,
   // size and props are optionals
   size: 3,
   props: (data) => ({
      title: "Average amount of t-shirt by order this month",
      value: data.average_quantity
   }),
};
```

The `description` value will be useful in a later exercise to show the name of items that the user can add to their dashboard. The `size` number is optional, and simply describes the size of the dashboard item that will be displayed. Finally, the `props` function is optional. If not given, we will simply give the `statistics` object as data. But if it is defined, it will be used to compute specific props for the component.

The goal is to replace the content of the dashboard with the following snippet:
```
<t t-foreach="items" t-as="item" t-key="item.id">
   <DashboardItem size="item.size || 1">
      <t t-set="itemProp" t-value="item.props ? item.props(statistics) : {'data': statistics}"/>
      <t t-component="item.Component" t-props="itemProp" />
   </DashboardItem>
</t>
```

Note that the above example features two advanced features of Owl: dynamic components and dynamic props.

We currently have two kinds of item components: number cards with a title and a number, and pie cards with some label and a pie chart.

1. Create and implement two components: `NumberCard` and `PieChartCard`, with the corresponding props.
2. Create a file `dashboard_items.js` in which you define and export a list of items, using `NumberCard` and `PieChartCard` to recreate our current dashboard.
3. Import that list of items in our `Dashboard` component, add it to the component, and update the template to use a `t-foreach` like shown above.
```
setup() {
   this.items = items;
}
```

And now, our dashboard template is generic!

- **tutorials/awesome_dashboard/static/src/dashboard/number_card/number_card.js**
```
/** @odoo-module */

import { Component } from "@odoo/owl";

export class NumberCard extends Component {
  static template = "awesome_dashboard.NumberCard";
  static props = {
    title: {
      type: String,
    },
    value: {
      type: Number,
    },
  };
}
```

- **tutorials/awesome_dashboard/static/src/dashboard/number_card/number_card.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_dashboard.NumberCard" owl="1">
        <t t-esc="props.title"/>
        <div class="fs-1 fw-bold text-success text-center">
            <t t-esc="props.value"/>
        </div>
    </t>
</templates>
```

- **tutorials/awesome_dashboard/static/src/dashboard/pie_chart_card/pie_chart_card.js**
```
/** @odoo-module */

import { Component } from "@odoo/owl";
import { PieChart } from "../pie_chart/pie_chart";

export class PieChartCard extends Component {
  static template = "awesome_dashboard.PieChartCard";
  static components = { PieChart };
  static props = {
    title: {
      type: String,
    },
    values: {
      type: Object,
    },
  };
}
```

- **tutorials/awesome_dashboard/static/src/dashboard/pie_chart_card/pie_chart_card.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_dashboard.PieChartCard" owl="1">
        <t t-esc="props.title"/>
        <PieChart data="props.values" label="''"/>
    </t>
</templates>
```

- **tutorials/awesome_dashboard/static/src/dashboard/dashboard_items.js**
```
/** @odoo-module */

import { NumberCard } from "./number_card/number_card";
import { PieChartCard } from "./pie_chart_card/pie_chart_card";

export const items = [
  {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    props: (data) => ({
      title: "Average amount of t-shirt by order this month",
      value: data.average_quantity,
    }),
  },
  {
    id: "average_time",
    description: "Average time for an order",
    Component: NumberCard,
    props: (data) => ({
      title:
        "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
      value: data.average_time,
    }),
  },
  {
    id: "number_new_orders",
    description: "New orders this month",
    Component: NumberCard,
    props: (data) => ({
      title: "Number of new orders this month",
      value: data.nb_new_orders,
    }),
  },
  {
    id: "cancelled_orders",
    description: "Cancelled orders this month",
    Component: NumberCard,
    props: (data) => ({
      title: "Number of cancelled orders this month",
      value: data.nb_cancelled_orders,
    }),
  },
  {
    id: "amount_new_orders",
    description: "amount orders this month",
    Component: NumberCard,
    props: (data) => ({
      title: "Total amount of new orders this month",
      value: data.total_amount,
    }),
  },
  {
    id: "pie_chart",
    description: "Shirt orders by size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
      title: "Shirt orders by size",
      values: data.orders_by_size,
    }),
  },
];
```

- **tutorials/awesome_dashboard/static/src/dashboard/dashboard.js**
```
/** @odoo-module **/
...
import { items } from "./dashboard_items";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };

  setup() {
...
    };
    this.items = items;
  }
...
```

- **tutorials/awesome_dashboard/static/src/dashboard/dashboard.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">

    <t t-name="awesome_dashboard.AwesomeDashboard">
        <Layout display="display" className="'o_dashboard h-100'">
            <t t-set-slot="layout-buttons">
                <button class="btn btn-primary" t-on-click="openCustomerView">Customers</button>
                <button class="btn btn-primary" t-on-click="openLeads">Leads</button>
            </t>
            <div class="d-flex flex-wrap" t-if="statistics.isReady">
                <t t-foreach="items" t-as="item" t-key="item.id">
                    <DashboardItem size="item.size || 1">
                        <t t-set="itemProp" t-value="item.props ? item.props(statistics) : {'data': statistics}"/>
                        <t t-component="item.Component" t-props="itemProp" />
                    </DashboardItem>
                </t>
            </div>
        </Layout>
    </t>

</templates>

```

## 10. Making our dashboard extensible

However, the content of our item list is still hardcoded. Let us fix that by using a registry:

1. Instead of exporting a list, register all dashboard items in a `awesome_dashboard` registry
2. Import all the items of the `awesome_dashboard` registry in the `Dashboard` component

The dashboard is now easily extensible. Any other Odoo addon that wants to register a new item to the dashboard can just add it to the registry.


- **tutorials/awesome_dashboard/static/src/dashboard/dashboard_items.js**
```
import { registry } from "@web/core/registry";

const items = [
...
]

items.forEach(item => {
    registry.category("awesome_dashboard").add(item.id, item);
});
```

- **tutorials/awesome_dashboard/static/src/dashboard/dashboard.js**
```
class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };

  setup() {
...
    this.items = registry.category("awesome_dashboard").getAll();
  }
```
