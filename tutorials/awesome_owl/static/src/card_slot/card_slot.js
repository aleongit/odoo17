/** @odoo-module **/

import { Component } from "@odoo/owl";

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
}
