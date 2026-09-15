# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFootwearQCInspection(FrappeTestCase):
	def test_defects_cannot_exceed_sample_size(self):
		doc = frappe.new_doc("Footwear QC Inspection")
		doc.sample_size = 5
		doc.defects_found = 6
		with self.assertRaises(frappe.ValidationError):
			doc.validate()

	def test_defects_within_sample_pass(self):
		doc = frappe.new_doc("Footwear QC Inspection")
		doc.sample_size = 10
		doc.defects_found = 3
		doc.validate()  # should not raise
