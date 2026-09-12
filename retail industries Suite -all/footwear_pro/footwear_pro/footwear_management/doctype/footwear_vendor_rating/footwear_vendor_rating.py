# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class FootwearVendorRating(Document):
    def validate(self):
        scores = [self.quality_score or 0, self.delivery_score or 0, self.price_score or 0]
        self.overall_rating = round(sum(scores) / 3, 2) if any(scores) else 0

