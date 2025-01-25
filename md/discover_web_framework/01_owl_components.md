# Chapter 1: Owl components

https://www.odoo.com/documentation/17.0/developer/tutorials/discover_js_framework/01_owl_components.html


- This chapter introduces the **Owl framework**, a tailor-made component system for Odoo
- https://github.com/odoo/owl
- The main building blocks of OWL are **components** and **templates**
- https://github.com/odoo/owl/blob/master/doc/reference/component.md
- https://github.com/odoo/owl/blob/master/doc/reference/templates.md


In Owl, every part of user interface is managed by a *component*: they hold the logic and define the *templates* that are used to render the user interface. In practice, a component is represented by a small *JavaScript class* subclassing the *Component class*.

To get started, you need a running Odoo server and a development environment setup. Before getting into the exercises, make sure you have followed all the steps described in this *tutorial introduction*.


-  💡 **Tip**:
- If you use *Chrome* as your web browser, you can install the `Owl Devtools` extension
- This extension provides many features to help you understand and profile any Owl application

In this chapter, we use the `awesome_owl` addon, which provides a simplified environment that only contains Owl and a few other files. The goal is to learn Owl itself, without relying on Odoo web client code.

- The solutions for each exercise of the chapter are hosted on the official Odoo tutorials repository
- It is recommended to try to solve them first without looking at the solution!
- https://github.com/odoo/tutorials/commits/17.0-discover-js-framework-solutions/awesome_owl


## Example: a `Counter` component

First, let us have a look at a simple example. The `Counter` component shown below is a component that maintains an internal number value, displays it, and updates it whenever the user clicks on the button.

```
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "my_module.Counter";

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;
    }
}
```

The `Counter` component specifies the name of a template that represents its html. It is written in *XML* using the *QWeb* language:

```
<templates xml:space="preserve">
   <t t-name="my_module.Counter">
      <p>Counter: <t t-esc="state.value"/></p>
      <button class="btn btn-primary" t-on-click="increment">Increment</button>
   </t>
</templates>
```

## 1. Displaying a counter

- http://192.168.1.60:8069/awesome_owl

- As a first exercise, let us modify the `Playground` component located in `awesome_owl/static/src/` to turn it into a counter
- To see the result, you can go to the `/awesome_owl` route with your browser

---

1. Modify `playground.js` so that it acts as a counter like in the example above
- Keep `Playground` for the class name
- You will need to use the `useState` hook so that the component is re-rendered whenever any part of the state object that has been read by this component is modified

2. In the same component, create an `increment` method

3. Modify the template in `playground.xml` so that it displays your counter variable
- Use `t-esc` to output the data
- https://github.com/odoo/owl/blob/master/doc/reference/templates.md#outputting-data

4. Add a button in the template and specify a `t-on-click` attribute in the button to trigger the `increment` method whenever the button is clicked
- https://github.com/odoo/owl/blob/master/doc/reference/event_handling.md#event-handling

---

- ⚠️ **Important**:
- Don’t forget `/** @odoo-module **/` in your JavaScript files
- https://www.odoo.com/documentation/17.0/developer/reference/frontend/javascript_modules.html#frontend-modules-native-js

---

- 💡 **Tip**:
- The Odoo JavaScript files downloaded by the browser are minified
- For debugging purpose, it’s easier when the files are not minified
- Switch to `debug mode with assets` so that the files are not minified
- https://www.odoo.com/documentation/17.0/applications/general/developer_mode.html#developer-mode-activation

---

- This exercise showcases an important feature of Owl: the **reactivity** system
- The `useState` function wraps a value in a proxy so Owl can keep track of which component needs which part of the state, so it can be updated whenever a value has been changed
- Try removing the `useState` function and see what happens.
- https://github.com/odoo/owl/blob/master/doc/reference/reactivity.md


- **tutorials/awesome_owl/static/src/playground.js**
```
import { Component, useState } from "@odoo/owl";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  setup() {
    this.state = useState({ counter: 0 });
  }

  increment() {
    this.state.counter++;
  }
}
```

- **tutorials/awesome_owl/static/src/playground.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_owl.playground">
        <div class="p-3">
            hello world
        </div>
        <div class="p-3">
            <p>Counter: <t t-esc="state.counter"/>
            </p>
            <button class="btn btn-primary" t-on-click="increment">
                Increment
            </button>
        </div>
    </t>
</templates>
```


## 2. Extract Counter in a sub component

- For now we have the logic of a counter in the `Playground` component, but it is not reusable
- Let us see how to create a **sub-component** from it:
- https://github.com/odoo/owl/blob/master/doc/reference/component.md#sub-components

---

1. Extract the counter code from the `Playground` component into a new `Counter` component

2. You can do it in the same file first, but once it’s done, update your code to move the `Counter` in its own folder and file
- Import it relatively from `./counter/counter`
- Make sure the template is in its own file, with the same name

3. Use `<Counter/>` in the template of the `Playground` component to add two counters in your playground

---

- 💡 **Tip**:
- By convention, most components code, template and css should have the same snake-cased name as the component
- For example, if we have a `TodoList` component, its code should be in `todo_list.js`, `todo_list.xml` and if necessary, `todo_list.scss`

---

- **tutorials/awesome_owl/static/src/counter/counter.js**
```
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
  static template = "awesome_owl.counter";

  setup() {
    this.state = useState({ counter: 0 });
  }

  increment() {
    this.state.counter++;
  }
}
```

- **tutorials/awesome_owl/static/src/counter/counter.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_owl.counter">
        <div class="p-3">
            <p>Counter: <t t-esc="state.counter"/>
            </p>
            <button class="btn btn-primary" t-on-click="increment">
                Increment
            </button>
        </div>
    </t>
</templates>
```

- **tutorials/awesome_owl/static/src/playground.js**
```
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter };
}
```

- **tutorials/awesome_owl/static/src/playground.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_owl.playground">
        <div class="p-3">
            hello world
        </div>
        <div class="d-flex justify-content-start">
            <Counter />
            <Counter />
        </div>
    </t>
</templates>
```


## 3. A simple Card component

- Components are really the most natural way to divide a complicated user interface into multiple reusable pieces
- But to make them truly useful, it is necessary to be able to communicate some information between them
- Let us see how a parent component can provide information to a sub component by using *attributes* (most commonly known as `props`)
- https://github.com/odoo/owl/blob/master/doc/reference/props.md

---

- The goal of this exercise is to create a `Card` component, that takes two *props*: `title` and `content`
- For example, here is how it could be used:
```
<Card title="'my title'" content="'some content'"/>
```

- The above example should produce some html using bootstrap that look like this:
```
<div class="card d-inline-block m-2" style="width: 18rem;">
    <div class="card-body">
        <h5 class="card-title">my title</h5>
        <p class="card-text">
         some content
        </p>
    </div>
</div>
```

1. Create a `Card` component
2. Import it in `Playground` and display a few cards in its template

---

- **tutorials/awesome_owl/static/src/card/card.js**
```
/** @odoo-module **/

import { Component } from "@odoo/owl";

export class Card extends Component {
  static template = "awesome_owl.card";
}
```

- **tutorials/awesome_owl/static/src/card/card.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_owl.card">
        <div class="card d-inline-block m-2" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">
                    <t t-esc="props.title"/>
                </h5>
                <p class="card-text">
                    <t t-esc="props.content"/>
                </p>
            </div>
        </div>
    </t>
</templates>
```

- **tutorials/awesome_owl/static/src/playground.js**
```
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card };
}
```

- **tutorials/awesome_owl/static/src/playground.xml**
```
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_owl.playground">
        <div class="p-3">
            hello world
        </div>
        <!-- counter -->
        <div class="d-flex justify-content-start">
            <Counter />
            <Counter />
        </div>
        <!-- card with props -->
        <div class="d-flex justify-content-start">
            <Card title="'card 1'" content="'content of card 1'"/>
            <Card title="'card 2'" content="'content of card 2'"/>
        </div>
    </t>
</templates>
```

## 4. Using `markup` to display html