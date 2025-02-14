/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";

export class TodoList extends Component {
  static template = "awesome_owl.todo_list";
  static components = { TodoItem };

  setup() {
    // this.todos = useState([
    //   { id: 1, description: "write tutorial", isCompleted: false },
    //   { id: 2, description: "buy milk", isCompleted: true },
    //   { id: 3, description: "save the world", isCompleted: false },
    // ]);
    this.todos = useState([]);
    this.nextId = 0;
    useAutofocus("input")
  }

  addTodo(ev) {
    if (ev.keyCode === 13 && ev.target.value != "") {
      this.todos.push({
        id: this.nextId++,
        description: ev.target.value,
        isCompleted: false,
      });
      ev.target.value = "";
    }
  }
}
