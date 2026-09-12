# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, nowdate

from fmcg_pro.fmcg_pro.utils import get_expiry_status


class FMCGBatchExpiryTracker(Document):
	def validate(self):
		self.update_expiry_status()

	def update_expiry_status(self):
		"""Compute days-to-expiry and status from the configured threshold."""
		if not self.expiry_date:
			self.days_to_expiry = None
			self.status = "Fresh"
			return

		settings = frappe.get_cached_doc("FMCG Pro Settings")
		self.days_to_expiry = date_diff(self.expiry_date, nowdate())
		self.status = get_expiry_status(
			self.days_to_expiry, settings.near_expiry_days or 30
		)

	def on_update(self):
		# keep the row fresh without requiring a full re-save later
		frappe.db.set_value(
			"FMCG Batch Expiry Tracker",
			self.name,
			{"days_to_expiry": self.days_to_expiry, "status": self.status},
			update_modified=False,
		)
