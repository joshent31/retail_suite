# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RoomMeasurementSheet(Document):
    def validate(self):
        for r in self.rooms:
            r.area_sqft = (r.length_ft or 0) * (r.width_ft or 0)

