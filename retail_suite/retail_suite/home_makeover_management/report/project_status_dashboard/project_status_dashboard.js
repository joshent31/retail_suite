// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Project Status Dashboard"] = {
	filters: [
		{
			fieldname: "workflow_state",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nLead\nConsultation\nDesign\nApproved\nExecution\nCompleted\nCancelled",
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
			fieldname: "project_type",
			label: __("Project Type"),
			fieldtype: "Select",
			options: "\nFull Home\nKitchen\nLiving Room\nBedroom\nOffice",
			default: "",
		},
	],
};
