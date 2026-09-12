# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "Production Order", "fieldname": "name", "fieldtype": "Link",
         "options": "Apparel Production Order", "width": 160},
        {"label": "Style", "fieldname": "style", "fieldtype": "Link",
         "options": "Apparel Style Master", "width": 140},
        {"label": "Qty to Produce", "fieldname": "qty_to_produce",
         "fieldtype": "Float", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Cutting Date", "fieldname": "cutting_date", "fieldtype": "Date",
         "width": 100},
        {"label": "Packing Date", "fieldname": "packing_date", "fieldtype": "Date",
         "width": 100},
    ]
    conditions = []
    values = {}
    if filters.get("status"):
        conditions.append("status = %(status)s")
        values["status"] = filters.get("status")
    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    data = frappe.db.sql(f"""
        SELECT name, style, qty_to_produce, status, cutting_date, packing_date
        FROM `tabApparel Production Order`
        {where}
        ORDER BY creation DESC
    """, values, as_dict=1)
    return columns, data
