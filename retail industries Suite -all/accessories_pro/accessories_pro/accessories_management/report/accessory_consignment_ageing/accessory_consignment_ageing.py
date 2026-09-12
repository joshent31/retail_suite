import frappe
from frappe.utils import date_diff, nowdate


def execute(filters=None):
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
    ]
    rows = frappe.db.sql("""
        SELECT name, supplier, consignment_date, workflow_state
        FROM `tabAccessory Consignment Stock`
        WHERE workflow_state != 'Settled'
        ORDER BY consignment_date ASC
    """, as_dict=1)
    for r in rows:
        r["age"] = date_diff(nowdate(), r.consignment_date) if r.consignment_date else 0
    return columns, rows
