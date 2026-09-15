# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_months, nowdate


class TestFootwearWarrantyClaim(FrappeTestCase):
	def test_warranty_window_computation(self):
		doc = frappe.new_doc("Footwear Warranty Claim")
		doc.purchase_date = "2026-01-15"
		doc.warranty_months = 6
		doc.compute_warranty_window()
		self.assertEqual(str(doc.warranty_valid_upto), "2026-07-15")

	def test_warranty_window_default_months(self):
		doc = frappe.new_doc("Footwear Warranty Claim")
		doc.purchase_date = nowdate()
		doc.warranty_months = None
		doc.compute_warranty_window()
		self.assertEqual(
			str(doc.warranty_valid_upto), str(add_months(nowdate(), 0))
		)
