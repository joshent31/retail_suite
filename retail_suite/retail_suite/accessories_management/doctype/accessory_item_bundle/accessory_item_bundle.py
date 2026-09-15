# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class AccessoryItemBundle(Document):
	def validate(self):
		self.validate_components()
		self.validate_price()

	def validate_components(self):
		if not self.components:
			frappe.throw(_("A bundle needs at least one component item"))
		seen = set()
		for c in self.components:
			if c.item in seen:
				frappe.throw(_("Component {0} is listed more than once").format(c.item))
			seen.add(c.item)
			if flt(c.qty) <= 0:
				frappe.throw(_("Row {0}: Component Qty must be greater than zero").format(c.idx))

	def validate_price(self):
		# warn (not block) when the bundle price undercuts the sum of component list rates
		total = 0
		for c in self.components:
			rate = flt(
				frappe.db.get_value("Item Price", {"item_code": c.item}, "price_list_rate")
			)
			total += rate * flt(c.qty)
		if total and flt(self.bundle_price) < total:
			frappe.msgprint(
				_("Bundle price ({0}) is below the component value ({1})").format(
					frappe.utils.fmt_money(self.bundle_price),
					frappe.utils.fmt_money(total),
				),
				indicator="orange",
			)


@frappe.whitelist()
def get_bundle_stock_availability(bundle_name, qty_needed=1):
	"""Max sellable bundles given current actual stock of each component."""
	qty_needed = flt(qty_needed) or 1
	bundle = frappe.get_doc("Accessory Item Bundle", bundle_name)

	limit = None
	insufficient = []
	for c in bundle.components:
		actual = get_actual_qty(c.item)
		can_make = int(actual / flt(c.qty)) if flt(c.qty) > 0 else 0
		if limit is None or can_make < limit:
			limit = can_make
		if actual < flt(c.qty) * qty_needed:
			insufficient.append(
				{"item": c.item, "required": flt(c.qty) * qty_needed, "available": actual}
			)

	return {
		"max_bundles_available": limit or 0,
		"can_fulfill": (limit or 0) >= qty_needed,
		"insufficient": insufficient,
	}


def get_actual_qty(item_code):
	from erpnext.stock.utils import get_stock_balance

	return flt(get_stock_balance(item_code))
