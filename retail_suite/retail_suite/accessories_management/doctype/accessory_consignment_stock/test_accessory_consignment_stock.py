# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestAccessoryConsignmentStock(FrappeTestCase):
	def _make_doc(self):
		doc = frappe.new_doc("Accessory Consignment Stock")
		doc.append("items", {"item": "_Test Item", "qty": 10, "qty_sold": 0})
		return doc

	def test_qty_must_be_positive(self):
		doc = self._make_doc()
		doc.items[0].qty = 0
		with self.assertRaises(frappe.ValidationError):
			doc.validate()

	def test_qty_sold_cannot_exceed_qty(self):
		doc = self._make_doc()
		doc.items[0].qty_sold = 11
		with self.assertRaises(frappe.ValidationError):
			doc.validate()

	def test_qty_remaining_computed(self):
		doc = self._make_doc()
		doc.items[0].qty_sold = 4
		doc.validate()
		self.assertEqual(doc.items[0].qty_remaining, 6)
