// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.ui.form.on("Footwear Warranty Claim", {
	refresh(frm) {
		if (frm.doc.docstatus === 1 && frm.doc.workflow_state === "Approved" && !frm.doc.delivery_note) {
			frm.add_custom_button(__("Create Delivery Note"), () => {
				frappe.model.open_mapped_doc({
					method: "retail_suite.footwear_management.doctype.footwear_warranty_claim.footwear_warranty_claim.make_delivery_note",
					frm: frm,
				});
			});
			frm.set_intro(__("Claim approved. Create the replacement Delivery Note above."));
		}
	},
	purchase_date(frm) {
		// client-side preview; the server recomputes on save
		if (frm.doc.purchase_date) {
			const months = frm.doc.warranty_months || 6;
			const d = new Date(frm.doc.purchase_date);
			d.setMonth(d.getMonth() + months);
			frm.set_value("warranty_valid_upto", d.toISOString().slice(0, 10));
		}
	},
	warranty_months(frm) {
		if (frm.doc.purchase_date) {
			const d = new Date(frm.doc.purchase_date);
			d.setMonth(d.getMonth() + (frm.doc.warranty_months || 6));
			frm.set_value("warranty_valid_upto", d.toISOString().slice(0, 10));
		}
	},
});
