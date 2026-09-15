// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Footwear Stock by Size Run"] = {
	filters: [
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
			default: "",
		},
		{
			fieldname: "style",
			label: __("Style"),
			fieldtype: "Link",
			options: "Footwear Style Master",
			default: "",
		},
	],
};
