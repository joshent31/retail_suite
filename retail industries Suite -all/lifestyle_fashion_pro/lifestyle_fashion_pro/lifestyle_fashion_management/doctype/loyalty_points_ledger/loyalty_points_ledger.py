# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LoyaltyPointsLedger(Document):
    def validate(self):
        prev = frappe.db.sql(
            """SELECT balance_points FROM `tabLoyalty Points Ledger`
               WHERE customer=%s AND docstatus=1
               ORDER BY transaction_date DESC, creation DESC LIMIT 1""",
            (self.customer,)
        )
        prev_balance = prev[0][0] if prev else 0
        delta = self.points if self.transaction_type == "Earned" else -self.points
        self.balance_points = (prev_balance or 0) + delta

