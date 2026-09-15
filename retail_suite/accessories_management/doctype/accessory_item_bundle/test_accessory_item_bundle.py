# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestAccessoryItemBundle(FrappeTestCase):
	def _make_doc(self):
		doc = frappe.new_doc("Accessory Item Bundle")
		doc.bundle_name = "_Test Bundle"
		doc.append("components", {"item": "_Test Item A", "qty": 2})
		doc.append("components", {"item": "_Test Item B", "qty": 1})
		return doc

	def test_duplicate_component_rejected(self):
		doc = self._make_doc()
		doc.append("components", {"item": "_Test Item A", "qty": 1})
		with self.assertRaises(frappe.ValidationError):
			doc.validate_components()

	def test_zero_qty_component_rejected(self):
		doc = self._make_doc()
		doc.components[0].qty = 0
		with self.assertRaises(frappe.ValidationError):
			doc.validate_components()

	def test_valid_components_pass(self):
		doc = self._make_doc()
		doc.validate_components()  # should not raise
