// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.ui.form.on("Accessory Item Bundle", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Check Stock Availability"), () => {
				frappe.prompt(
					{ fieldname: "qty_needed", fieldtype: "Int", label: __("Bundles Needed"), default: 1 },
					(values) => {
						frappe.call({
							method: "accessories_pro.accessories_pro.accessories_management.doctype.accessory_item_bundle.accessory_item_bundle.get_bundle_stock_availability",
							args: {
								bundle_name: frm.doc.name,
								qty_needed: values.qty_needed,
							},
							callback: (r) => {
								if (!r.message) return;
								const d = r.message;
								if (d.can_fulfill) {
									frappe.msgprint({
										message: __("Yes - {0} bundle(s) can be built from current stock.", [d.max_bundles_available]),
										indicator: "green",
									});
								} else {
									const missing = (d.insufficient || [])
										.map((x) => `<li>${frappe.utils.escape_html(x.item)}: ${x.available} / ${x.required}</li>`)
										.join("");
									frappe.msgprint({
										title: __("Insufficient Stock"),
										message:
											__("Only {0} bundle(s) can be built. Shortages:<ul>{1}</ul>", [
												d.max_bundles_available,
												missing,
											]) || __("Only {0} bundle(s) can be built.", [d.max_bundles_available]),
										indicator: "red",
									});
								}
							},
						});
					}
				);
			});
		}
	},
});
