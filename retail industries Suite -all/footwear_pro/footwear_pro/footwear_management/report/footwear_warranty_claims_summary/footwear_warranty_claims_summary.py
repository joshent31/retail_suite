import frappe


def execute(filters=None):
    columns = [
        {"label": "Claim", "fieldname": "name", "fieldtype": "Link",
         "options": "Footwear Warranty Claim", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link",
         "options": "Customer", "width": 150},
        {"label": "Item", "fieldname": "item", "fieldtype": "Link",
         "options": "Item", "width": 150},
        {"label": "Status", "fieldname": "workflow_state", "fieldtype": "Data",
         "width": 120},
    ]
    data = frappe.db.sql("""
        SELECT name, customer, item, workflow_state
        FROM `tabFootwear Warranty Claim`
        ORDER BY creation DESC
    """, as_dict=1)
    return columns, data
