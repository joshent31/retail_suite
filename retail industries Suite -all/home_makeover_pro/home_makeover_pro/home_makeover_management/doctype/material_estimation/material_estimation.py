# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MaterialEstimation(Document):
    def validate(self):
        for i in self.items:
            i.amount = (i.estimated_qty or 0) * (i.estimated_rate or 0)
        self.total_estimated_cost = sum(i.amount or 0 for i in self.items)

