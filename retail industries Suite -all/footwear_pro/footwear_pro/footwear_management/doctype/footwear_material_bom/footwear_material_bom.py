# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FootwearMaterialBOM(Document):
    def validate(self):
        for m in self.materials:
            m.amount = (m.qty or 0) * (m.rate or 0)
        self.total_cost = sum(m.amount or 0 for m in self.materials)

