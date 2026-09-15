import frappe
from frappe.utils import nowdate


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": "Item", "fieldname": "item", "fieldtype": "Link",
		 "options": "Item", "width": 150},
		{"label": "Batch", "fieldname": "batch", "fieldtype": "Link",
		 "options": "Batch", "width": 120},
		{"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link",
		 "options": "Warehouse", "width": 140},
		{"label": "Expiry Date", "fieldname": "expiry_date", "fieldtype": "Date",
		 "width": 110},
		{"label": "Days to Expiry", "fieldname": "days_to_expiry",
		 "fieldtype": "Int", "width": 110},
		{"label": "Qty", "fieldname": "qty", "fieldtype": "Float", "width": 90},
	]

	conditions = ["status IN ('Near Expiry', 'Expired')"]
	values = {}
	if filters.get("warehouse"):
		conditions.append("warehouse = %(warehouse)s")
		values["warehouse"] = filters["warehouse"]
	if filters.get("item"):
		conditions.append("item = %(item)s")
		values["item"] = filters["item"]
	if filters.get("status"):
		conditions.remove("status IN ('Near Expiry', 'Expired')")
		conditions.append("status = %(status)s")
		values["status"] = filters["status"]

	data = frappe.db.sql(
		f"""
		SELECT item, batch, warehouse, expiry_date, days_to_expiry, qty
		FROM `tabFMCG Batch Expiry Tracker`
		WHERE {' AND '.join(conditions)}
		ORDER BY expiry_date ASC
	""",
		values,
		as_dict=1,
	)

	# days_to_expiry is a snapshot; recompute against today for accuracy
	for row in data:
		if row.expiry_date:
			row.days_to_expiry = frappe.utils.date_diff(row.expiry_date, nowdate())

	return columns, data
