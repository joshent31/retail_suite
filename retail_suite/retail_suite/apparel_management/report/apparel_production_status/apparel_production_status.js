// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Apparel Production Status"] = {
	filters: [
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nDraft\nCutting\nSewing\nFinishing\nPacked\nCompleted\nCancelled",
			default: "",
		},
		{
			fieldname: "from_date",
			label: __("From Packing Date"),
			fieldtype: "Date",
			default: "",
		},
		{
			fieldname: "to_date",
			label: __("To Packing Date"),
			fieldtype: "Date",
			default: "",
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: "",
		},
	],
};
