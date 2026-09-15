# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class FMCGVanSalesEntry(Document):
	def validate(self):
		self.validate_items()
		self.calculate_totals()

	def validate_items(self):
		if not self.items:
			frappe.throw(_("At least one item is required for a Van Sales Entry"))
		for i in self.items:
			if (i.qty or 0) <= 0:
				frappe.throw(_("Row {0}: Qty must be greater than zero").format(i.idx))

	def calculate_totals(self):
		for i in self.items:
			i.amount = flt(i.qty) * flt(i.rate)
		self.total_amount = sum(flt(i.amount) for i in self.items)


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	"""Create a Sales Invoice (draft) from a Van Sales Entry, mapped item by item."""
	from frappe.model.mapper import get_mapped_doc

	def postprocess(doc, method=None):
		doc.run_method("set_missing_values")

	return get_mapped_doc(
		"FMCG Van Sales Entry",
		source_name,
		{
			"FMCG Van Sales Entry": {
				"doctype": "Sales Invoice",
				"field_map": {},
				"validation": {"docstatus": ["=", 1]},
			},
			"FMCG Van Sales Item": {
				"doctype": "Sales Invoice Item",
				"field_map": {"item": "item_code", "qty": "qty", "rate": "rate"},
			},
		},
		target_doc,
		postprocess,
	)
