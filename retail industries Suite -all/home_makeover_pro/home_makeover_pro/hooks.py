from . import __version__ as app_version

app_name = "home_makeover_pro"
app_title = "Home Makeover Pro"
app_publisher = "Your Organization"
app_description = "End-to-end project tracking, room measurements, material estimation, contractor assignment and milestone billing for home makeover/interiors businesses on ERPNext."
app_email = "admin@example.com"
app_license = "MIT"
required_apps = ["frappe/erpnext"]

# Includes in <head>
# ------------------
# app_include_css = "/assets/home_makeover_pro/css/home_makeover_pro.css"
# app_include_js = "/assets/home_makeover_pro/js/home_makeover_pro.js"

# Fixtures
# --------
# Exported as data via `bench --site [site] export-fixtures`
fixtures = [
	{"dt": "Role", "filters": [["name", "in", ['Home Makeover Manager', 'Home Makeover Designer']]]},
	{"dt": "Notification", "filters": [["module", "=", "Home Makeover Management"]]},
	{"dt": "Workflow", "filters": [["document_type", "in", ['Home Makeover Project']]]},
	{"dt": "Print Format", "filters": [["module", "=", "Home Makeover Management"]]},
]

# Installation
# ------------
# before_install = "home_makeover_pro.install.before_install"
# after_install = "home_makeover_pro.install.after_install"

# Document Events
# ----------------
# Hook on document methods and events
#
# doc_events = {
# 	"*": {
# 		"on_update": "home_makeover_pro.utils.on_doc_update"
# 	}
# }

# Scheduled Tasks
# ----------------
scheduler_events = {
	"daily": [
		"home_makeover_pro.tasks.daily"
	]
}
