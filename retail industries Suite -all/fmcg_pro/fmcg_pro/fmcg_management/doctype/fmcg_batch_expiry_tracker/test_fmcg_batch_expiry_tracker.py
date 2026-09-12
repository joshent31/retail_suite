# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

from fmcg_pro.fmcg_pro.utils import get_expiry_status


class TestFMCGBatchExpiryTracker(FrappeTestCase):
	def test_status_mapping(self):
		self.assertEqual(get_expiry_status(-5), "Expired")
		self.assertEqual(get_expiry_status(0), "Near Expiry")
		self.assertEqual(get_expiry_status(15), "Near Expiry")
		self.assertEqual(get_expiry_status(30), "Near Expiry")
		self.assertEqual(get_expiry_status(31), "Fresh")
		self.assertEqual(get_expiry_status(200), "Fresh")

	def test_status_mapping_custom_threshold(self):
		self.assertEqual(get_expiry_status(45, near_expiry_days=60), "Near Expiry")
		self.assertEqual(get_expiry_status(61, near_expiry_days=60), "Fresh")
