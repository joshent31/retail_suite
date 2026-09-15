# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ApparelReturnExchangeRequest(Document):
	def validate(self):
		self.validate_item_on_invoice()
		self.validate_duplicate_request()
		if flt(self.refund_amount) < 0:
			frappe.throw(_("Refund Amount cannot be negative"))

	def validate_item_on_invoice(self):
		if self.sales_invoice and self.item:
			exists = frappe.db.exists(
				"Sales Invoice Item",
				{"parent": self.sales_invoice, "item_code": self.item, "docstatus": 1},
			)
			if not exists:
				frappe.throw(
					_("Item {0} is not on Sales Invoice {1}").format(self.item, self.sales_invoice)
				)

	def validate_duplicate_request(self):
		if self.sales_invoice and self.item:
			existing = frappe.db.exists(
				"Apparel Return Exchange Request",
				{
					"sales_invoice": self.sales_invoice,
					"item": self.item,
					"status": ["in", ["Requested", "Approved"]],
					"name": ["!=", self.name],
				},
			)
			if existing:
				frappe.throw(
					_("An active return/exchange request {0} already exists for this item").format(
						existing
					)
				)
