import frappe


def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = [
		{"label": "Customer", "fieldname": "customer", "fieldtype": "Link",
		 "options": "Customer", "width": 180},
		{"label": "Current Balance", "fieldname": "balance_points",
		 "fieldtype": "Int", "width": 130},
		{"label": "Last Transaction", "fieldname": "transaction_date",
		 "fieldtype": "Date", "width": 130},
	]

	conditions = ["l1.docstatus = 1"]
	values = {}
	if filters.get("customer"):
		conditions.append("l1.customer = %(customer)s")
		values["customer"] = filters["customer"]
	if filters.get("min_balance"):
		conditions.append("l1.balance_points >= %(min_balance)s")
		values["min_balance"] = filters["min_balance"]

	data = frappe.db.sql(
		f"""
		SELECT l1.customer, l1.balance_points, l1.transaction_date
		FROM `tabLoyalty Points Ledger` l1
		INNER JOIN (
			SELECT customer, MAX(transaction_date) AS max_date
			FROM `tabLoyalty Points Ledger`
			WHERE docstatus = 1
			GROUP BY customer
		) l2 ON l1.customer = l2.customer AND l1.transaction_date = l2.max_date
		WHERE {' AND '.join(conditions)}
		ORDER BY l1.balance_points DESC
	""",
		values,
		as_dict=1,
	)
	return columns, data
