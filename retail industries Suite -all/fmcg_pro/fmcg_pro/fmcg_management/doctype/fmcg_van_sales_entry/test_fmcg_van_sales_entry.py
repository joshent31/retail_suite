# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFMCGVanSalesEntry(FrappeTestCase):
	def test_totals_calculated(self):
		doc = frappe.new_doc("FMCG Van Sales Entry")
		doc.append("items", {"item": "_Test Item", "qty": 2, "rate": 50})
		doc.append("items", {"item": "_Test Item 2", "qty": 1, "rate": 100})
		doc.calculate_totals()
		self.assertEqual(doc.items[0].amount, 100)
		self.assertEqual(doc.total_amount, 200)

	def test_empty_items_rejected(self):
		doc = frappe.new_doc("FMCG Van Sales Entry")
		with self.assertRaises(frappe.ValidationError):
			doc.validate_items()

	def test_zero_qty_rejected(self):
		doc = frappe.new_doc("FMCG Van Sales Entry")
		doc.append("items", {"item": "_Test Item", "qty": 0, "rate": 50})
		with self.assertRaises(frappe.ValidationError):
			doc.validate_items()
