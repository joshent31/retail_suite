// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Footwear Warranty Claims Summary"] = {
	filters: [
		{
			fieldname: "workflow_state",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nOpen\nUnder Review\nApproved\nRejected\nResolved",
			default: "",
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
			default: "",
		},
		{
			fieldname: "item",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item",
			default: "",
		},
	],
};
