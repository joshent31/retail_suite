// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.ui.form.on("Apparel Production Order", {
	refresh(frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Create Stock Entry"), () => {
				frappe.model.open_mapped_doc({
					method: "retail_suite.apparel_management.doctype.apparel_production_order.apparel_production_order.make_stock_entry",
					frm: frm,
				});
			});
		}
	},
	qty_to_produce(frm) {
		calc_fabric(frm);
	},
	fabric_consumption_meters(frm) {
		calc_fabric(frm);
	},
	wastage_percent(frm) {
		calc_fabric(frm);
	},
});

function calc_fabric(frm) {
	if (frm.doc.qty_to_produce && frm.doc.fabric_consumption_meters) {
		const total =
			(frm.doc.qty_to_produce || 0) *
			(frm.doc.fabric_consumption_meters || 0) *
			(1 + (frm.doc.wastage_percent || 0) / 100.0);
		frm.set_value("total_fabric_required", Math.round(total * 1000) / 1000);
	}
}
