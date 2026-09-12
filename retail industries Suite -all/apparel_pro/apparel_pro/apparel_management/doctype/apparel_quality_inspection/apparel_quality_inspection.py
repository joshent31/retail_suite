# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ApparelQualityInspection(Document):
    def validate(self):
        self.defects_found = sum(d.quantity or 0 for d in self.defect_details)

