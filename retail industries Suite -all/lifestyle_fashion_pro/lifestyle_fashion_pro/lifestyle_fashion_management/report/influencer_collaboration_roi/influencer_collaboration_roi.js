// Copyright (c) 2026, Your Organization and contributors
// For license information, please see license.txt

frappe.query_reports["Influencer Collaboration ROI"] = {
	filters: [
		{
			fieldname: "platform",
			label: __("Platform"),
			fieldtype: "Select",
			options: "\nInstagram\nYouTube\nTikTok\nFacebook\nX (Twitter)\nBlog/Other",
			default: "",
		},
		{
			fieldname: "collection",
			label: __("Collection"),
			fieldtype: "Link",
			options: "Fashion Collection Master",
			default: "",
		},
	],
};
