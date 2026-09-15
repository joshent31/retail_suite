// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Accessory Consignment Ageing"] = {
	filters: [
		{
			fieldname: "supplier",
			label: __("Supplier"),
			fieldtype: "Link",
			options: "Supplier",
			default: "",
		},
		{
			fieldname: "older_than_days",
			label: __("Older Than (days)"),
			fieldtype: "Int",
			default: "",
		},
	],
};
