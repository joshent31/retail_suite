# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": "Production Order", "fieldname": "name", "fieldtype": "Link",
		 "options": "Apparel Production Order", "width": 160},
		{"label": "Style", "fieldname": "style", "fieldtype": "Link",
		 "options": "Apparel Style Master", "width": 140},
		{"label": "Company", "fieldname": "company", "fieldtype": "Link",
		 "options": "Company", "width": 130},
		{"label": "Qty to Produce", "fieldname": "qty_to_produce",
		 "fieldtype": "Float", "width": 120},
		{"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
		{"label": "Cutting Date", "fieldname": "cutting_date", "fieldtype": "Date",
		 "width": 100},
		{"label": "Packing Date", "fieldname": "packing_date", "fieldtype": "Date",
		 "width": 100},
	]

	conditions = ["1=1"]
	values = {}
	if filters.get("status"):
		conditions.append("status = %(status)s")
		values["status"] = filters["status"]
	if filters.get("company"):
		conditions.append("company = %(company)s")
		values["company"] = filters["company"]
	if filters.get("from_date"):
		conditions.append("packing_date >= %(from_date)s")
		values["from_date"] = filters["from_date"]
	if filters.get("to_date"):
		conditions.append("packing_date <= %(to_date)s")
		values["to_date"] = filters["to_date"]

	data = frappe.db.sql(
		f"""
		SELECT name, style, company, qty_to_produce, status, cutting_date, packing_date
		FROM `tabApparel Production Order`
		WHERE {' AND '.join(conditions)}
		ORDER BY creation DESC
	""",
		values,
		as_dict=1,
	)
	return columns, data
