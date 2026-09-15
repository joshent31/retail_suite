// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Near Expiry Stock Alert"] = {
	filters: [
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
			default: "",
		},
		{
			fieldname: "item",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
			default: "",
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "Near Expiry\nExpired",
			default: "Near Expiry",
		},
	],
};
