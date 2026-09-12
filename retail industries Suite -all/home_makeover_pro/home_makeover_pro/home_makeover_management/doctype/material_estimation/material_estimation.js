// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.ui.form.on("Material Estimation", {
	refresh(frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Create Material Request"), () => {
				frappe.call({
					method: "home_makeover_pro.home_makeover_pro.home_makeover_management.doctype.material_estimation.material_estimation.make_material_request",
					args: { source_name: frm.doc.name },
					freeze: true,
					freeze_message: __("Creating Material Request..."),
					callback: (r) => {
						if (r.message) {
							frappe.set_route("Form", "Material Request", r.message);
						}
					},
				});
			});
		}
	},
});

frappe.ui.form.on("Material Estimation Item", {
	estimated_qty(frm, cdt, cdn) {
		calc_amount(cdt, cdn);
	},
	estimated_rate(frm, cdt, cdn) {
		calc_amount(cdt, cdn);
	},
});

function calc_amount(cdt, cdn) {
	const row = locals[cdt][cdn];
	frappe.model.set_value(
		cdt,
		cdn,
		"amount",
		(row.estimated_qty || 0) * (row.estimated_rate || 0)
	);
}
