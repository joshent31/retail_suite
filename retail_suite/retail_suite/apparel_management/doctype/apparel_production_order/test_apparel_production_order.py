# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestApparelProductionOrder(FrappeTestCase):
	def test_fabric_requirement_calculation(self):
		"""total = qty x consumption x (1 + wastage%)"""
		doc = frappe.new_doc("Apparel Production Order")
		doc.qty_to_produce = 100
		doc.fabric_consumption_meters = 1.5
		doc.wastage_percent = 10
		doc.calculate_fabric_requirement()
		self.assertEqual(doc.total_fabric_required, 165.0)

	def test_fabric_requirement_zero_when_missing_inputs(self):
		doc = frappe.new_doc("Apparel Production Order")
		doc.qty_to_produce = 100
		doc.fabric_consumption_meters = None
		doc.wastage_percent = None
		doc.calculate_fabric_requirement()
		self.assertEqual(doc.total_fabric_required, 0)

	def test_validate_rejects_zero_qty(self):
		doc = frappe.new_doc("Apparel Production Order")
		doc.qty_to_produce = 0
		with self.assertRaises(frappe.ValidationError):
			doc.validate()

	def test_validate_rejects_backwards_dates(self):
		doc = frappe.new_doc("Apparel Production Order")
		doc.qty_to_produce = 10
		doc.cutting_date = "2026-05-10"
		doc.sewing_completion_date = "2026-05-01"
		with self.assertRaises(frappe.ValidationError):
			doc.validate()
