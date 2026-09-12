// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Loyalty Points Balance Summary"] = {
	filters: [
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
			default: "",
		},
		{
			fieldname: "min_balance",
			label: __("Min Balance"),
			fieldtype: "Int",
			default: "",
		},
	],
};
