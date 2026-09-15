# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFMCGSchemePromotion(FrappeTestCase):
	def test_new_doc_instantiates(self):
		"""Smoke test: controller imports cleanly and doctype metadata loads."""
		doc = frappe.new_doc("FMCG Scheme Promotion")
		self.assertEqual(doc.doctype, "FMCG Scheme Promotion")
