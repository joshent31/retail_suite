# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def get_expiry_status(days_to_expiry: int, near_expiry_days: int = 30) -> str:
	"""Pure helper: map days-to-expiry to a status string."""
	if days_to_expiry < 0:
		return "Expired"
	if days_to_expiry <= near_expiry_days:
		return "Near Expiry"
	return "Fresh"


def get_role_emails(role: str) -> list[str]:
	users = frappe.get_all(
		"Has Role", filters={"role": role, "parenttype": "User"}, pluck="parent"
	)
	if not users:
		return []
	return frappe.get_all(
		"User", filters={"name": ["in", users], "enabled": 1}, pluck="email"
	)


def run():
	"""Recompute expiry statuses (they go stale otherwise) and alert on near-expiry stock."""
	settings = frappe.get_cached_doc("FMCG Pro Settings")
	near_days = settings.near_expiry_days or 30
	today = frappe.utils.nowdate()

	trackers = frappe.get_all(
		"FMCG Batch Expiry Tracker", fields=["name", "expiry_date", "status"]
	)
	for t in trackers:
		if not t.expiry_date:
			continue
		days = frappe.utils.date_diff(t.expiry_date, today)
		status = get_expiry_status(days, near_days)
		if status != t.status:
			frappe.db.set_value(
				"FMCG Batch Expiry Tracker",
				t.name,
				{"days_to_expiry": days, "status": status},
				update_modified=False,
			)

	if not settings.alert_near_expiry:
		return

	rows = frappe.get_all(
		"FMCG Batch Expiry Tracker",
		filters={"status": ["in", ["Near Expiry", "Expired"]]},
		fields=["item", "batch", "warehouse", "expiry_date", "days_to_expiry"],
		order_by="expiry_date asc",
		limit_page_length=0,
	)
	if not rows:
		return

	table = "".join(
		"<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
			frappe.escape(r.item or ""),
			frappe.escape(r.batch or ""),
			frappe.escape(r.warehouse or ""),
			r.expiry_date,
			r.days_to_expiry,
		)
		for r in rows
	)
	message = (
		"<p>{}</p>"
		"<table class='table table-bordered'><tr><th>Item</th><th>Batch</th>"
		"<th>Warehouse</th><th>Expiry Date</th><th>Days to Expiry</th></tr>{}</table>"
	).format(
		_("The following batches are near expiry or already expired:"),
		table,
	)

	recipients = get_role_emails("FMCG Manager")
	if recipients:
		frappe.sendmail(
			recipients=recipients,
			subject=_("FMCG Near-Expiry Stock Alert: {} batches").format(len(rows)),
			message=message,
		)
