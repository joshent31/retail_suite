import frappe
from frappe.utils import date_diff, nowdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": "Consignment", "fieldname": "name", "fieldtype": "Link",
		 "options": "Accessory Consignment Stock", "width": 150},
		{"label": "Supplier", "fieldname": "supplier", "fieldtype": "Link",
		 "options": "Supplier", "width": 150},
		{"label": "Consignment Date", "fieldname": "consignment_date",
		 "fieldtype": "Date", "width": 120},
		{"label": "Age (Days)", "fieldname": "age", "fieldtype": "Int", "width": 100},
		{"label": "Status", "fieldname": "workflow_state", "fieldtype": "Data",
		 "width": 120},
		{"label": "Settlement Amount", "fieldname": "settlement_amount",
		 "fieldtype": "Currency", "width": 130},
	]

	conditions = ["workflow_state != 'Settled'"]
	values = {}
	if filters.get("supplier"):
		conditions.append("supplier = %(supplier)s")
		values["supplier"] = filters["supplier"]
	if filters.get("older_than_days"):
		conditions.append("consignment_date <= %(cutoff)s")
		values["cutoff"] = frappe.utils.add_days(nowdate(), -int(filters["older_than_days"]))

	rows = frappe.db.sql(
		f"""
		SELECT name, supplier, consignment_date, workflow_state, settlement_amount
		FROM `tabAccessory Consignment Stock`
		WHERE {' AND '.join(conditions)}
		ORDER BY consignment_date ASC
	""",
		values,
		as_dict=1,
	)
	for r in rows:
		r["age"] = date_diff(nowdate(), r.consignment_date) if r.consignment_date else 0
	return columns, rows
