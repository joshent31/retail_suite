# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestInfluencerBrandCollaboration(FrappeTestCase):
	def test_new_doc_instantiates(self):
		"""Smoke test: controller imports cleanly and doctype metadata loads."""
		doc = frappe.new_doc("Influencer Brand Collaboration")
		self.assertEqual(doc.doctype, "Influencer Brand Collaboration")
