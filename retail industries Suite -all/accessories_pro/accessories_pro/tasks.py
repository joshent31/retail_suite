# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import add_days, date_diff, nowdate

from accessories_pro.accessories_pro.utils import notify_role


def daily():
	"""Flag consignments sitting unsold for over 30 days (ageing stock)."""
	cutoff = add_days(nowdate(), -30)
	stale = frappe.get_all(
		"Accessory Consignment Stock",
		filters={
			"docstatus": 1,
			"workflow_state": ["in", ["Received", "Partially Sold"]],
			"consignment_date": ["<", cutoff],
		},
		fields=["name", "supplier", "consignment_date"],
		order_by="consignment_date asc",
	)
	if not stale:
		return

	rows = "".join(
		"<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
			frappe.escape(s.name),
			frappe.escape(s.supplier or ""),
			s.consignment_date,
			date_diff(nowdate(), s.consignment_date),
		)
		for s in stale
	)
	message = (
		"<p>{}</p>"
		"<table class='table table-bordered'><tr><th>Consignment</th><th>Supplier</th>"
		"<th>Consignment Date</th><th>Age (days)</th></tr>{}</table>"
	).format(_("These consignments have been in stock for over 30 days:"), rows)

	notify_role(
		"Accessories Manager",
		_("Accessories: {} consignments ageing").format(len(stale)),
		message,
	)
