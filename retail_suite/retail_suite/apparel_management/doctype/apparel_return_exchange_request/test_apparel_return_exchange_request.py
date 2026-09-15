# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestApparelReturnExchangeRequest(FrappeTestCase):
	def test_negative_refund_rejected(self):
		doc = frappe.new_doc("Apparel Return Exchange Request")
		doc.refund_amount = -100
		with self.assertRaises(frappe.ValidationError):
			doc.validate()

	def test_zero_refund_passes(self):
		doc = frappe.new_doc("Apparel Return Exchange Request")
		doc.refund_amount = 0
		doc.validate()  # no invoice checks fire without sales_invoice/item
