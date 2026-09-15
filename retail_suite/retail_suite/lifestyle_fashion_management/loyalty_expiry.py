# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate


def run():
	"""Create 'Expired' ledger entries for earned points past their expiry date.

	Customers with no explicit expiry set keep points indefinitely; earned
	entries carrying an expiry_date in the past are swept once.
	"""
	today = nowdate()
	stale = frappe.get_all(
		"Loyalty Points Ledger",
		filters={
			"docstatus": 1,
			"transaction_type": "Earned",
			"expiry_date": ["<", today],
		},
		fields=["name", "customer", "points", "expiry_date"],
	)
	if not stale:
		return

	# idempotency guard: skip customers whose points were already swept for that date
	already = set(
		frappe.get_all(
			"Loyalty Points Ledger",
			filters={"transaction_type": "Expired", "expiry_date": stale[0].expiry_date},
			pluck="reversal_of",
		)
	)

	for row in stale:
		if row.name in already:
			continue
		expiry_entry = frappe.new_doc("Loyalty Points Ledger")
		expiry_entry.customer = row.customer
		expiry_entry.transaction_type = "Expired"
		expiry_entry.points = row.points
		expiry_entry.expiry_date = row.expiry_date
		expiry_entry.transaction_date = today
		expiry_entry.reversal_of = row.name
		expiry_entry.insert(ignore_permissions=True)
		expiry_entry.submit()
