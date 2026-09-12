# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ApparelProductionOrder(Document):
	def validate(self):
		if flt(self.qty_to_produce) <= 0:
			frappe.throw(_("Qty to Produce must be greater than zero"))
		if self.sewing_completion_date and self.cutting_date:
			if self.sewing_completion_date < self.cutting_date:
				frappe.throw(_("Sewing Completion Date cannot be before Cutting Date"))
		if self.packing_date and self.sewing_completion_date:
			if self.packing_date < self.sewing_completion_date:
				frappe.throw(_("Packing Date cannot be before Sewing Completion Date"))
		self.calculate_fabric_requirement()

	def calculate_fabric_requirement(self):
		"""Total fabric = qty x consumption per piece, inflated by wastage %."""
		if self.qty_to_produce and self.fabric_consumption_meters:
			self.total_fabric_required = flt(self.qty_to_produce) * flt(
				self.fabric_consumption_meters
			) * (1 + flt(self.wastage_percent) / 100.0)
		else:
			self.total_fabric_required = 0


@frappe.whitelist()
def make_stock_entry(source_name, target_doc=None):
	"""Create a Material Transfer / Manufacture Stock Entry from a submitted Production Order."""
	from frappe.model.mapper import get_mapped_doc

	def postprocess(doc, method=None):
		doc.stock_entry_type = "Manufacture"
		doc.set_missing_values()

	return get_mapped_doc(
		"Apparel Production Order",
		source_name,
		{
			"Apparel Production Order": {
				"doctype": "Stock Entry",
				"field_map": {"name": "apparel_pro_production_order"},
				"validation": {"docstatus": ["=", 1]},
			},
		},
		target_doc,
		postprocess,
	)
