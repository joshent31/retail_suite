# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import add_days, nowdate

from footwear_pro.footwear_pro.utils import notify_role


def daily():
	"""Nudge the Footwear Manager about warranty claims stuck in review."""
	cutoff = add_days(nowdate(), -7)
	stale = frappe.get_all(
		"Footwear Warranty Claim",
		filters={
			"docstatus": 0,
			"workflow_state": ["in", ["Open", "Under Review"]],
			"creation": ["<", cutoff],
		},
		fields=["name", "customer", "workflow_state"],
		order_by="creation asc",
	)
	if not stale:
		return

	rows = "".join(
		"<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
			frappe.escape(s.name), frappe.escape(s.customer or ""), s.workflow_state
		)
		for s in stale
	)
	message = (
		"<p>{}</p>"
		"<table class='table table-bordered'><tr><th>Claim</th><th>Customer</th>"
		"<th>Status</th></tr>{}</table>"
	).format(_("These warranty claims have been open for more than 7 days:"), rows)

	notify_role(
		"Footwear Manager",
		_("Footwear: {} warranty claims awaiting action").format(len(stale)),
		message,
	)
