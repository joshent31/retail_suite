import frappe


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": "Claim", "fieldname": "name", "fieldtype": "Link",
		 "options": "Footwear Warranty Claim", "width": 150},
		{"label": "Customer", "fieldname": "customer", "fieldtype": "Link",
		 "options": "Customer", "width": 150},
		{"label": "Item", "fieldname": "item", "fieldtype": "Link",
		 "options": "Item", "width": 150},
		{"label": "Purchase Date", "fieldname": "purchase_date", "fieldtype": "Date",
		 "width": 110},
		{"label": "Warranty Valid Upto", "fieldname": "warranty_valid_upto",
		 "fieldtype": "Date", "width": 130},
		{"label": "Status", "fieldname": "workflow_state", "fieldtype": "Data",
		 "width": 120},
	]

	conditions = ["1=1"]
	values = {}
	if filters.get("workflow_state"):
		conditions.append("workflow_state = %(workflow_state)s")
		values["workflow_state"] = filters["workflow_state"]
	if filters.get("customer"):
		conditions.append("customer = %(customer)s")
		values["customer"] = filters["customer"]
	if filters.get("item"):
		conditions.append("item = %(item)s")
		values["item"] = filters["item"]

	data = frappe.db.sql(
		f"""
		SELECT name, customer, item, purchase_date, warranty_valid_upto, workflow_state
		FROM `tabFootwear Warranty Claim`
		WHERE {' AND '.join(conditions)}
		ORDER BY creation DESC
	""",
		values,
		as_dict=1,
	)
	return columns, data
