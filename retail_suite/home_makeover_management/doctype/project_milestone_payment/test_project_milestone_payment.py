# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestProjectMilestonePayment(FrappeTestCase):
	def _make_doc(self, percentages):
		doc = frappe.new_doc("Project Milestone Payment")
		for idx, pct in enumerate(percentages, start=1):
			doc.append("milestones", {"milestone_name": f"M{idx}", "percentage": pct})
		return doc

	def test_total_percentage_over_100_rejected(self):
		doc = self._make_doc([60, 60])
		with self.assertRaises(frappe.ValidationError):
			doc.validate_milestones()

	def test_total_percentage_within_100_passes(self):
		doc = self._make_doc([40, 60])
		doc.validate_milestones()  # should not raise
