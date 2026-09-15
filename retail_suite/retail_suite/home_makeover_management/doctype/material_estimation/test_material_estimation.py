# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestMaterialEstimation(FrappeTestCase):
	def test_amounts_and_total_calculated(self):
		doc = frappe.new_doc("Material Estimation")
		doc.append("items", {"item": "_Test Item", "estimated_qty": 4, "estimated_rate": 25})
		doc.append("items", {"item": "_Test Item 2", "estimated_qty": 1, "estimated_rate": 100})
		doc.validate()
		self.assertEqual(doc.items[0].amount, 100)
		self.assertEqual(doc.total_estimated_cost, 200)

	def test_empty_items_rejected(self):
		doc = frappe.new_doc("Material Estimation")
		with self.assertRaises(frappe.ValidationError):
			doc.validate()

	def test_negative_qty_rejected(self):
		doc = frappe.new_doc("Material Estimation")
		doc.append("items", {"item": "_Test Item", "estimated_qty": -1, "estimated_rate": 10})
		with self.assertRaises(frappe.ValidationError):
			doc.validate()
