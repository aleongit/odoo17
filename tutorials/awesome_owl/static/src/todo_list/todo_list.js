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
    useAutofocus("input");
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

  toggleTodo(todoId) {
    const todo = this.todos.find((todo) => todo.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  }

  removeTodo(todoId) {
    // amb splice; trobar index i modificar array
    // const todoIndex = this.todos.findIndex((todo) => todo.id === todoId);
    // if (todoIndex >= 0) {
    //   this.todos.splice(todoIndex, 1);
    // }
    
    // amb filtered; filtrar amb nova array, i afegir-la a array d'estar eliminant el què tenia
    // fem el que fem, sempre necessitem modificar array gestionada per useState
    const filtered = this.todos.filter(todo => todo.id !== todoId);
    this.todos.splice(0, this.todos.length, ...filtered); // Actualitza l'array original
  }

  removeTodoAll(ev) {
    if (ev) {
      this.todos.splice(0, this.todos.length);
    }
  }
}
