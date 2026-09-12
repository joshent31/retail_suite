# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_months, nowdate


class FootwearWarrantyClaim(Document):
	def validate(self):
		self.compute_warranty_window()
		self.validate_warranty_window()
		self.validate_replacement()

	def compute_warranty_window(self):
		"""Warranty end = purchase date + configured months (default 6)."""
		if self.purchase_date:
			months = int(self.warranty_months or 0)
			self.warranty_valid_upto = add_months(self.purchase_date, months)
		else:
			self.warranty_valid_upto = None

	def validate_warranty_window(self):
		if self.override_warranty_check:
			return
		if self.warranty_valid_upto and nowdate() > str(self.warranty_valid_upto):
			frappe.throw(
				_("Warranty expired on {0}. Enable 'Override Warranty Check' to file anyway.").format(
					self.warranty_valid_upto
				)
			)

	def validate_replacement(self):
		if self.workflow_state == "Approved" and not self.replacement_item:
			frappe.throw(_("Replacement Item is required to approve a warranty claim"))
		if self.replacement_item and self.replacement_item == self.item:
			# allowed, but replacement must exist
			if not frappe.db.exists("Item", self.replacement_item):
				frappe.throw(_("Replacement Item {0} does not exist").format(self.replacement_item))


@frappe.whitelist()
def make_delivery_note(source_name, target_doc=None):
	"""Create a zero-rated Delivery Note for the approved warranty replacement."""
	from frappe.model.mapper import get_mapped_doc

	def postprocess(doc, method=None):
		for item in doc.items:
			item.rate = 0
			item.amount = 0
		doc.run_method("set_missing_values")

	return get_mapped_doc(
		"Footwear Warranty Claim",
		source_name,
		{
			"Footwear Warranty Claim": {
				"doctype": "Delivery Note",
				"validation": {"docstatus": ["=", 1]},
			},
		},
		target_doc,
		postprocess,
	)
