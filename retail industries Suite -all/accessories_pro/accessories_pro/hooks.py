
app_name = "accessories_pro"
app_title = "Accessories Pro"
app_publisher = "Retail Industry Suite"
app_description = "Category masters, item bundles, material composition, consignment stock and returns for accessories retail on ERPNext."
app_email = "admin@example.com"
app_license = "MIT"
required_apps = ["frappe/erpnext"]

# Includes in <head>
# ------------------
# app_include_css = "/assets/accessories_pro/css/accessories_pro.css"
# app_include_js = "/assets/accessories_pro/js/accessories_pro.js"

# Fixtures
# --------
# Exported as data via `bench --site [site] export-fixtures`
fixtures = [
	{"dt": "Role", "filters": [["name", "in", ['Accessories Manager', 'Accessories User']]]},
	{"dt": "Notification", "filters": [["module", "=", "Accessories Management"]]},
	{"dt": "Workflow", "filters": [["document_type", "in", ['Accessory Consignment Stock']]]},
	{"dt": "Print Format", "filters": [["module", "=", "Accessories Management"]]},
	{"dt": "Number Card", "filters": [["name", "in", ['Accessories Active Consignments']]]},
	{"dt": "Dashboard Chart", "filters": [["name", "in", ['Accessories Consignments by Status']]]},
]

# Installation
# ------------
before_install = "accessories_pro.accessories_pro.install.before_install"
after_uninstall = "accessories_pro.accessories_pro.install.after_uninstall"

# Document Events
# ----------------
doc_events = {
	"Accessory Consignment Stock": {
		"on_update": "accessories_pro.accessories_pro.utils.sync_workflow_status",
	}
}

# Scheduled Tasks
# ----------------
scheduler_events = {
	"daily": [
		"accessories_pro.accessories_pro.tasks.daily"
	]
}
