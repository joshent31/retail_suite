# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class MaterialEstimation(Document):
	def validate(self):
		if not self.items:
			frappe.throw(_("At least one material item is required"))
		for i in self.items:
			i.amount = flt(i.estimated_qty) * flt(i.estimated_rate)
			if flt(i.estimated_qty) < 0:
				frappe.throw(_("Row {0}: Estimated Qty cannot be negative").format(i.idx))
		self.total_estimated_cost = sum(flt(i.amount) for i in self.items)


@frappe.whitelist()
def make_material_request(source_name, target_doc=None):
	"""Create a draft Material Request from a submitted Material Estimation."""
	frappe.only_for(("Home Makeover Manager", "System Manager"))

	source = frappe.get_doc("Material Estimation", source_name)
	if source.docstatus != 1:
		frappe.throw(_("Only submitted Material Estimations can create a Material Request"))

	request = frappe.new_doc("Material Request")
	request.material_request_type = "Purchase"
	request.home_makeover_material_estimation = source.name

	for i in source.items:
		request.append(
			"items",
			{
				"item_code": i.item,
				"qty": flt(i.estimated_qty),
				"uom": i.uom,
				"rate": flt(i.estimated_rate),
				"schedule_date": frappe.utils.add_days(frappe.utils.nowdate(), 7),
			},
		)

	request.set_missing_values()
	request.insert(ignore_permissions=True)

	frappe.msgprint(
		_("Material Request {0} created").format(frappe.bold(request.name))
	)
	return request.name
