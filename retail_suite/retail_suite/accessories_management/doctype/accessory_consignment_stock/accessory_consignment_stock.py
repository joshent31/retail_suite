# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class AccessoryConsignmentStock(Document):
	def validate(self):
		if not self.items:
			frappe.throw(_("At least one consignment item is required"))
		for d in self.items:
			if flt(d.qty) <= 0:
				frappe.throw(_("Row {0}: Qty must be greater than zero").format(d.idx))
			if flt(d.qty_sold) > flt(d.qty):
				frappe.throw(
					_("Row {0}: Qty Sold ({1}) cannot exceed consigned Qty ({2})").format(
						d.idx, d.qty_sold, d.qty
					)
				)
			d.qty_remaining = flt(d.qty) - flt(d.qty_sold)

	def on_update(self):
		# roll the workflow forward automatically when everything is sold
		if (
			self.docstatus == 1
			and self.workflow_state in ("Received", "Partially Sold")
			and all(flt(d.qty_sold) >= flt(d.qty) for d in self.items)
		):
			frappe.db.set_value(
					"Accessory Consignment Stock", self.name, "workflow_state", "Partially Sold"
				)


@frappe.whitelist()
def settle_consignment(source_name):
	"""Create a Purchase Invoice payable to the supplier for the sold consignment qty."""
	frappe.only_for(("Accessories Manager", "System Manager"))

	doc = frappe.get_doc("Accessory Consignment Stock", source_name)
	if doc.docstatus != 1:
		frappe.throw(_("Submit the consignment record before settling"))
	if doc.workflow_state == "Settled":
		frappe.throw(_("This consignment is already settled"))

	sold_rows = [d for d in doc.items if flt(d.qty_sold) > 0]
	if not sold_rows:
		frappe.throw(_("No sold quantity to settle against"))

	invoice = frappe.new_doc("Purchase Invoice")
	invoice.supplier = doc.supplier
	invoice.accessories_consignment_stock = doc.name
	invoice.set_warehouse = doc.warehouse

	settlement_amount = 0
	for d in sold_rows:
		amount = flt(d.qty_sold) * flt(d.rate)
		settlement_amount += amount
		invoice.append(
			"items",
			{
				"item_code": d.item,
				"qty": flt(d.qty_sold),
				"rate": flt(d.rate),
				"warehouse": doc.warehouse,
			},
		)

	invoice.set_missing_values()
	invoice.calculate_taxes_and_totals()
	invoice.insert(ignore_permissions=True)

	frappe.db.set_value(
		"Accessory Consignment Stock",
		doc.name,
		{
			"workflow_state": "Settled",
			"purchase_invoice": invoice.name,
			"settlement_amount": settlement_amount,
		},
	)

	frappe.msgprint(
		_("Purchase Invoice {0} created for {1}").format(
			frappe.bold(invoice.name), frappe.utils.fmt_money(settlement_amount)
		)
	)
	return invoice.name
