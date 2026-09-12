# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe


def sync_workflow_status(doc, method=None):
	"""Mirror workflow_state into a plain `status` field when both exist."""
	if not getattr(doc, "workflow_state", None):
		return
	if hasattr(doc, "status") and doc.status != doc.workflow_state:
		doc.db_set("status", doc.workflow_state, update_modified=False)


def get_role_emails(role: str) -> list[str]:
	users = frappe.get_all(
		"Has Role", filters={"role": role, "parenttype": "User"}, pluck="parent"
	)
	if not users:
		return []
	return frappe.get_all(
		"User", filters={"name": ["in", users], "enabled": 1}, pluck="email"
	)


def notify_role(role: str, subject: str, message: str):
	recipients = get_role_emails(role)
	if recipients:
		frappe.sendmail(recipients=recipients, subject=subject, message=message)
