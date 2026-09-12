import frappe


def execute(filters=None):
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
    data = frappe.db.sql("""
        SELECT item, batch, warehouse, expiry_date, days_to_expiry, qty
        FROM `tabFMCG Batch Expiry Tracker`
        WHERE status IN ('Near Expiry', 'Expired')
        ORDER BY expiry_date ASC
    """, as_dict=1)
    return columns, data
