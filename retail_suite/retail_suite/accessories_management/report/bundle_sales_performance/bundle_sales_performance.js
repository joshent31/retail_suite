// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Bundle Sales Performance"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: "",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: "",
		},
	],
};
