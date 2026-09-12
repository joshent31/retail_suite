# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FMCGBatchExpiryTracker(Document):
    def validate(self):
        from frappe.utils import date_diff, nowdate
        if self.expiry_date:
            self.days_to_expiry = date_diff(self.expiry_date, nowdate())
            if self.days_to_expiry < 0:
                self.status = "Expired"
            elif self.days_to_expiry <= 30:
                self.status = "Near Expiry"
            else:
                self.status = "Fresh"

