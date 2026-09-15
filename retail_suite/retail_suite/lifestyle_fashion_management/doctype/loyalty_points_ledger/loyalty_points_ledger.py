# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, nowdate


class LoyaltyPointsLedger(Document):
	def validate(self):
		self.validate_points()
		self.validate_expiry()
		self.compute_balance()

	def validate_points(self):
		if flt(self.points) <= 0:
			frappe.throw(_("Points must be greater than zero"))
		if self.transaction_type == "Redeemed" and self.reference_invoice:
			# prevent redeeming twice against the same invoice
			existing = frappe.db.exists(
				"Loyalty Points Ledger",
				{
					"reference_invoice": self.reference_invoice,
					"transaction_type": "Redeemed",
					"docstatus": ["<", 2],
					"name": ["!=", self.name or ""],
				},
			)
			if existing:
				frappe.throw(
					_("Points already redeemed against invoice {0} (entry {1})").format(
						self.reference_invoice, existing
					)
				)

	def validate_expiry(self):
		if self.transaction_type == "Expired" and not self.expiry_date:
			self.expiry_date = nowdate()

	def compute_balance(self):
		"""Running balance per customer.

		Takes SELECT ... FOR UPDATE on the customer's latest submitted row so two
		concurrent submissions cannot read the same previous balance. The lock is
		held until the enclosing transaction commits, which is the standard
		Frappe pattern (see ERPNext's GL Entry).
		"""
		self.transaction_date = self.transaction_date or nowdate()

		# acquire the row lock (result unused; side effect is the lock)
		frappe.db.sql(
			"""
			SELECT name FROM `tabLoyalty Points Ledger`
			WHERE customer = %s AND docstatus = 1
			ORDER BY transaction_date DESC, creation DESC
			LIMIT 5
			FOR UPDATE
			""",
			(self.customer,),
		)

		prev_balance = self.get_previous_balance()
		delta = flt(self.points)
		if self.transaction_type in ("Redeemed", "Expired"):
			delta = -delta
		self.balance_points = int(prev_balance + delta)

	def get_previous_balance(self):
		row = frappe.db.sql(
			"""
			SELECT balance_points FROM `tabLoyalty Points Ledger`
			WHERE customer = %s AND docstatus = 1
			ORDER BY transaction_date DESC, creation DESC
			LIMIT 1
			""",
			(self.customer,),
		)
		return row[0][0] if row else 0

	def on_submit(self):
		if self.balance_points < 0:
			frappe.throw(
				_("Cannot submit: redemption would take {0}'s balance negative ({1})").format(
					self.customer, self.balance_points
				)
			)

	def on_cancel(self):
		# reverse this entry with an opposite adjustment row
		reversal = frappe.new_doc("Loyalty Points Ledger")
		reversal.customer = self.customer
		reversal.transaction_type = (
			"Earned" if self.transaction_type in ("Redeemed", "Expired") else "Redeemed"
		)
		reversal.points = self.points
		reversal.reference_invoice = self.reference_invoice
		reversal.transaction_date = nowdate()
		reversal.reversal_of = self.name
		reversal.insert(ignore_permissions=True)
		reversal.submit()

		frappe.msgprint(
			_("Reversal entry {0} created for cancelled ledger {1}").format(
				frappe.bold(reversal.name), frappe.bold(self.name)
			)
		)
