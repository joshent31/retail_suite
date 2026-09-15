# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class FootwearQCInspection(Document):
	def validate(self):
		self.validate_defects()

	def validate_defects(self):
		if flt(self.sample_size) > 0 and flt(self.defects_found) > flt(self.sample_size):
			frappe.throw(
				_("Defects found ({0}) cannot exceed sample size ({1})").format(
					self.defects_found, self.sample_size
				)
			)
