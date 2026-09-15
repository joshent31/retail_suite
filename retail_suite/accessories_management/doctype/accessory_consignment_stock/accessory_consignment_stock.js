// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.ui.form.on("Accessory Consignment Stock", {
	refresh(frm) {
		if (
			frm.doc.docstatus === 1 &&
			frm.doc.workflow_state !== "Settled" &&
			frm.doc.workflow_state !== "Returned"
		) {
			frm.add_custom_button(__("Settle with Supplier"), () => {
				frappe.call({
					method: "retail_suite.accessories_management.doctype.accessory_consignment_stock.accessory_consignment_stock.settle_consignment",
					args: { source_name: frm.doc.name },
					freeze: true,
					freeze_message: __("Creating Purchase Invoice..."),
					callback: (r) => {
						if (r.message) {
							frm.reload_doc();
							frappe.set_route("Form", "Purchase Invoice", r.message);
						}
					},
				});
			});
		}
	},
});
