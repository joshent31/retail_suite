// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Van Sales Summary by Route"] = {
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
		{
			fieldname: "route",
			label: __("Route"),
			fieldtype: "Link",
			options: "FMCG Route Beat Plan",
			default: "",
		},
		{
			fieldname: "salesperson",
			label: __("Salesperson"),
			fieldtype: "Link",
			options: "Employee",
			default: "",
		},
	],
};
