# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestApparelQualityInspection(FrappeTestCase):
	def test_defects_found_is_summed(self):
		doc = frappe.new_doc("Apparel Quality Inspection")
		doc.append("defect_details", {"defect_type": "Stitch", "quantity": 2})
		doc.append("defect_details", {"defect_type": "Hole", "quantity": 3})
		doc.sample_size = 10
		doc.result = "Pass"
		doc.validate()
		self.assertEqual(doc.defects_found, 5)

	def test_defects_cannot_exceed_sample_size(self):
		doc = frappe.new_doc("Apparel Quality Inspection")
		doc.append("defect_details", {"defect_type": "Stitch", "quantity": 12})
		doc.sample_size = 10
		doc.result = "Pass"
		with self.assertRaises(frappe.ValidationError):
			doc.validate()

	def test_critical_defect_requires_fail(self):
		doc = frappe.new_doc("Apparel Quality Inspection")
		doc.append("defect_details", {"defect_type": "Tear", "quantity": 1, "severity": "Critical"})
		doc.sample_size = 10
		doc.result = "Pass"
		with self.assertRaises(frappe.ValidationError):
			doc.validate()
