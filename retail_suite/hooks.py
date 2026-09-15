# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

app_name = "retail_suite"
app_title = "Retail Industry Suite"
app_publisher = "Retail Industry Suite"
app_description = "Six retail industry verticals (Apparel, Footwear, Accessories, Home Makeover, Lifestyle & Fashion, FMCG) for ERPNext."
app_email = "admin@example.com"
app_license = "mit"
required_apps = ["frappe/erpnext"]

# Fixtures
# --------
fixtures = [
	{"dt": "Role", "filters": [["name", "in", ["Apparel Manager", "Apparel User", "Footwear Manager", "Footwear User", "Accessories Manager", "Accessories User", "Home Makeover Manager", "Home Makeover Designer", "Fashion Manager", "Fashion Stylist", "FMCG Manager", "FMCG User"]]]},
	{"dt": "Notification", "filters": [["module", "in", ["Apparel Management", "Footwear Management", "Accessories Management", "Home Makeover Management", "Lifestyle Fashion Management", "Fmcg Management"]]]},
	{"dt": "Workflow", "filters": [["document_type", "in", ["Apparel Production Order", "Footwear Warranty Claim", "Accessory Consignment Stock", "Home Makeover Project", "Influencer Brand Collaboration", "FMCG Scheme Promotion"]]]},
	{"dt": "Print Format", "filters": [["module", "in", ["Apparel Management", "Footwear Management", "Accessories Management", "Home Makeover Management", "Lifestyle Fashion Management", "Fmcg Management"]]]},
	{"dt": "Number Card", "filters": [["name", "in", ["Apparel Open Production Orders", "Footwear Open Warranty Claims", "Accessories Active Consignments", "Home Makeover Active Projects", "Lifestyle Active Collaborations", "FMCG Near Expiry Batches"]]]},
	{"dt": "Dashboard Chart", "filters": [["name", "in", ["Apparel Production by Status", "Footwear Claims by Status", "Accessories Consignments by Status", "Home Makeover Projects by Status", "Lifestyle Collaborations by Status", "FMCG Batches by Status"]]]},
]

# Installation
# ------------
before_install = "retail_suite.install.before_install"
after_uninstall = "retail_suite.install.after_uninstall"

# Document Events
# ----------------
doc_events = {
	"Apparel Production Order": {
		"on_update": "retail_suite.utils.sync_workflow_status",
	},
	"Footwear Warranty Claim": {
		"on_update": "retail_suite.utils.sync_workflow_status",
	},
	"Accessory Consignment Stock": {
		"on_update": "retail_suite.utils.sync_workflow_status",
	},
	"Home Makeover Project": {
		"on_update": "retail_suite.utils.sync_workflow_status",
	},
	"Influencer Brand Collaboration": {
		"on_update": "retail_suite.utils.sync_workflow_status",
	},
	"FMCG Scheme Promotion": {
		"on_update": "retail_suite.utils.sync_workflow_status",
	},
}

# Scheduled Tasks
# ----------------
scheduler_events = {
	"daily": [
		"retail_suite.tasks.daily",
	],
}
