import frappe


def execute(filters=None):
    columns = [
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link",
         "options": "Customer", "width": 180},
        {"label": "Current Balance", "fieldname": "balance_points",
         "fieldtype": "Int", "width": 130},
        {"label": "Last Transaction", "fieldname": "transaction_date",
         "fieldtype": "Date", "width": 130},
    ]
    data = frappe.db.sql("""
        SELECT l1.customer, l1.balance_points, l1.transaction_date
        FROM `tabLoyalty Points Ledger` l1
        INNER JOIN (
            SELECT customer, MAX(transaction_date) AS max_date
            FROM `tabLoyalty Points Ledger`
            WHERE docstatus = 1
            GROUP BY customer
        ) l2 ON l1.customer = l2.customer AND l1.transaction_date = l2.max_date
        WHERE l1.docstatus = 1
        ORDER BY l1.balance_points DESC
    """, as_dict=1)
    return columns, data
