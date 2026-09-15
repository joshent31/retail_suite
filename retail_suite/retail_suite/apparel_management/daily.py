# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import nowdate

from retail_suite.utils import notify_role


def run():
	"""Flag production orders still in progress past their packing date."""
	overdue = frappe.get_all(
		"Apparel Production Order",
		filters={
			"docstatus": 0,
			"status": ["not in", ["Completed", "Cancelled"]],
			"packing_date": ["<", nowdate()],
		},
		fields=["name", "style", "packing_date", "status"],
		order_by="packing_date asc",
	)
	if not overdue:
		return

	rows = "".join(
		"<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
			frappe.escape(o.name),
			frappe.escape(o.style or ""),
			o.packing_date,
			frappe.escape(o.status or ""),
		)
		for o in overdue
	)
	message = (
		"<p>{}</p>"
		"<table class='table table-bordered'><tr><th>Order</th><th>Style</th>"
		"<th>Packing Date</th><th>Status</th></tr>{}</table>"
	).format(_("These production orders are overdue:"), rows)

	notify_role(
		"Apparel Manager",
		_("Apparel: {} overdue production orders").format(len(overdue)),
		message,
	)
