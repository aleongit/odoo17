/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class CardSlot extends Component {
  static template = "awesome_owl.card_slot";
  static props = {
    title: String,
    slots: {
      type: Object,
      shape: {
        default: true,
      },
    },
  };

  setup() {
    this.state = useState({ isOpen: true });
  }

  toggle() {
    this.state.isOpen = !this.state.isOpen;
    console.log(this.state.open);
  }
}
