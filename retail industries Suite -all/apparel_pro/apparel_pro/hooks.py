from . import __version__ as app_version

app_name = "apparel_pro"
app_title = "Apparel Pro"
app_publisher = "Your Organization"
app_description = "Style masters, size charts, production tracking, QC and returns for apparel retail on ERPNext."
app_email = "admin@example.com"
app_license = "MIT"
required_apps = ["frappe/erpnext"]

# Includes in <head>
# ------------------
# app_include_css = "/assets/apparel_pro/css/apparel_pro.css"
# app_include_js = "/assets/apparel_pro/js/apparel_pro.js"

# Fixtures
# --------
# Exported as data via `bench --site [site] export-fixtures`
fixtures = [
	{"dt": "Role", "filters": [["name", "in", ['Apparel Manager', 'Apparel User']]]},
	{"dt": "Notification", "filters": [["module", "=", "Apparel Management"]]},
	{"dt": "Workflow", "filters": [["document_type", "in", ['Apparel Production Order']]]},
	{"dt": "Print Format", "filters": [["module", "=", "Apparel Management"]]},
]

# Installation
# ------------
# before_install = "apparel_pro.install.before_install"
# after_install = "apparel_pro.install.after_install"

# Document Events
# ----------------
# Hook on document methods and events
#
# doc_events = {
# 	"*": {
# 		"on_update": "apparel_pro.utils.on_doc_update"
# 	}
# }

# Scheduled Tasks
# ----------------
scheduler_events = {
	"daily": [
		"apparel_pro.tasks.daily"
	]
}
