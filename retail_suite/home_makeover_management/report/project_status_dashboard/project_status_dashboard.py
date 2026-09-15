import frappe


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": "Project", "fieldname": "name", "fieldtype": "Link",
		 "options": "Home Makeover Project", "width": 150},
		{"label": "Customer", "fieldname": "customer", "fieldtype": "Link",
		 "options": "Customer", "width": 150},
		{"label": "Type", "fieldname": "project_type", "fieldtype": "Data", "width": 110},
		{"label": "Status", "fieldname": "workflow_state", "fieldtype": "Data",
		 "width": 110},
		{"label": "Budget Estimate", "fieldname": "budget_estimate",
		 "fieldtype": "Currency", "width": 130},
		{"label": "Start Date", "fieldname": "start_date", "fieldtype": "Date",
		 "width": 100},
		{"label": "Expected End", "fieldname": "expected_end_date", "fieldtype": "Date",
		 "width": 110},
	]

	conditions = ["1=1"]
	values = {}
	if filters.get("workflow_state"):
		conditions.append("workflow_state = %(workflow_state)s")
		values["workflow_state"] = filters["workflow_state"]
	if filters.get("customer"):
		conditions.append("customer = %(customer)s")
		values["customer"] = filters["customer"]
	if filters.get("project_type"):
		conditions.append("project_type = %(project_type)s")
		values["project_type"] = filters["project_type"]

	data = frappe.db.sql(
		f"""
		SELECT name, customer, project_type, workflow_state,
		       budget_estimate, start_date, expected_end_date
		FROM `tabHome Makeover Project`
		WHERE {' AND '.join(conditions)}
		ORDER BY creation DESC
	""",
		values,
		as_dict=1,
	)
	return columns, data
