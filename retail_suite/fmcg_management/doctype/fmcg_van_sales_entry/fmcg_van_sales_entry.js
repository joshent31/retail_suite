// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.ui.form.on("FMCG Van Sales Entry", {
	refresh(frm) {
		if (frm.doc.docstatus === 1 && !frm.doc.sales_invoice) {
			frm.add_custom_button(__("Create Sales Invoice"), () => {
				frappe.model.open_mapped_doc({
					method: "retail_suite.fmcg_management.doctype.fmcg_van_sales_entry.fmcg_van_sales_entry.make_sales_invoice",
					frm: frm,
				});
			});
		}
	},
});

frappe.ui.form.on("FMCG Van Sales Item", {
	qty(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
	rate(frm, cdt, cdn) {
		calculate_amount(frm, cdt, cdn);
	},
});

function calculate_amount(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	frappe.model.set_value(cdt, cdn, "amount", (row.qty || 0) * (row.rate || 0));
}
