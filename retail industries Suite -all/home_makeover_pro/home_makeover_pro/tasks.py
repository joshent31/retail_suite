# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import add_days, date_diff, nowdate

from home_makeover_pro.home_makeover_pro.utils import notify_role


def daily():
	"""Remind managers about milestones due within 3 days or overdue."""
	rows = frappe.db.sql(
		"""
		SELECT pmd.parent, pmd.milestone_name, pmd.due_date, pmd.status
		FROM `tabProject Milestone Detail` pmd
		JOIN `tabProject Milestone Payment` pmp ON pmp.name = pmd.parent
		WHERE pmp.docstatus = 0
		  AND pmd.status = 'Pending'
		  AND pmd.due_date IS NOT NULL
		  AND pmd.due_date <= %(cutoff)s
		ORDER BY pmd.due_date ASC
	""",
		{"cutoff": add_days(nowdate(), 3)},
		as_dict=1,
	)
	if not rows:
		return

	today = nowdate()
	overdue = [r for r in rows if date_diff(r.due_date, today) < 0]
	upcoming = [r for r in rows if date_diff(r.due_date, today) >= 0]

	def table(items):
		return "".join(
			"<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
				frappe.escape(i.parent),
				frappe.escape(i.milestone_name or ""),
				i.due_date,
				frappe.escape(i.status),
			)
			for i in items
		)

	header = "<tr><th>Milestone Payment</th><th>Milestone</th><th>Due Date</th><th>Status</th></tr>"
	parts = []
	if overdue:
		parts.append(
			"<p><b>{}</b></p><table class='table table-bordered'>{}{}</table>".format(
				_("Overdue milestones:"), header, table(overdue)
			)
		)
	if upcoming:
		parts.append(
			"<p><b>{}</b></p><table class='table table-bordered'>{}{}</table>".format(
				_("Milestones due within 3 days:"), header, table(upcoming)
			)
		)

	notify_role(
		"Home Makeover Manager",
		_("Home Makeover: {} milestones need attention").format(len(rows)),
		"".join(parts),
	)
