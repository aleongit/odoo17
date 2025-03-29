/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { CardSlot } from "./card_slot/card_slot";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";
  static components = { Counter, Card, CardSlot, TodoList };

  setup() {
    this.html1 = "<div class='text-primary'>some content</div>";
    this.html2 = markup("<div class='text-primary'>some content</div>");
    this.state = useState({ sum: 0 });
  }

  incrementSum() {
    this.state.sum++;
  }
}
