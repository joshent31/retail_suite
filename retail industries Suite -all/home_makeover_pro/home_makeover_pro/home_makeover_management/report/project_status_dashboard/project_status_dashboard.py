import frappe


def execute(filters=None):
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
        {"label": "Expected End", "fieldname": "expected_end_date",
         "fieldtype": "Date", "width": 110},
    ]
    data = frappe.db.sql("""
        SELECT name, customer, project_type, workflow_state,
               budget_estimate, expected_end_date
        FROM `tabHome Makeover Project`
        ORDER BY creation DESC
    """, as_dict=1)
    return columns, data
