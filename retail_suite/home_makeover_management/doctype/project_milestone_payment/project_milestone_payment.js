// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.ui.form.on("Project Milestone Payment", {
	refresh(frm) {
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__("Create Sales Invoice"), () => {
				frappe.call({
					method: "retail_suite.home_makeover_management.doctype.project_milestone_payment.project_milestone_payment.make_sales_invoice",
					args: { source_name: frm.doc.name },
					freeze: true,
					freeze_message: __("Creating Sales Invoice..."),
					callback: (r) => {
						if (r.message) {
							frappe.set_route("Form", "Sales Invoice", r.message);
						}
					},
				});
			});
		}
	},
});

frappe.ui.form.on("Project Milestone Detail", {
	percentage(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (frm.doc.project && row.percentage) {
			frappe.db.get_value(
				"Home Makeover Project",
				frm.doc.project,
				"budget_estimate",
				(budget) => {
					if (budget && budget.budget_estimate) {
						frappe.model.set_value(
							cdt,
							cdn,
							"amount",
							(flt(row.percentage) / 100.0) * flt(budget.budget_estimate)
						);
					}
				}
			);
		}
	},
});

function flt(v) {
	return parseFloat(v) || 0;
}
