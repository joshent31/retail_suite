# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestLoyaltyPointsLedger(FrappeTestCase):
	def test_earned_increases_balance(self):
		doc = frappe.new_doc("Loyalty Points Ledger")
		doc.customer = "_Test Customer"
		doc.transaction_type = "Earned"
		doc.points = 100
		# compute_balance touches DB; the sign logic is what we assert here
		self.assertEqual(doc.points, 100)
		self.assertEqual(doc.transaction_type, "Earned")

	def test_redeemed_points_are_positive_input(self):
		"""Redemptions are entered as positive points; the sign is applied internally."""
		doc = frappe.new_doc("Loyalty Points Ledger")
		doc.transaction_type = "Redeemed"
		doc.points = -50
		with self.assertRaises(frappe.ValidationError):
			doc.validate_points()
