# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ApparelQualityInspection(Document):
	def validate(self):
		self.defects_found = sum(flt(d.quantity) for d in self.defect_details)
		self.validate_defect_quantities()
		self.validate_critical_defects()

	def validate_defect_quantities(self):
		if self.sample_size and self.defects_found > self.sample_size:
			frappe.throw(
				_("Defects found ({0}) cannot exceed sample size ({1})").format(
					self.defects_found, self.sample_size
				)
			)

	def validate_critical_defects(self):
		critical = [d for d in self.defect_details if d.severity == "Critical"]
		if critical and self.result != "Fail":
			frappe.throw(
				_("A critical defect requires Result to be 'Fail' (row {0})").format(
					critical[0].idx
				)
			)
