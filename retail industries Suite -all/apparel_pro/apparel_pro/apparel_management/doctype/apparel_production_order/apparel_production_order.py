# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ApparelProductionOrder(Document):
    def validate(self):
        if self.qty_to_produce <= 0:
            frappe.throw("Qty to Produce must be greater than zero")

    def on_update(self):
        # keep plain status field mirroring workflow_state for easy reporting
        if self.workflow_state and self.status != self.workflow_state:
            self.db_set("status", self.workflow_state, update_modified=False)

