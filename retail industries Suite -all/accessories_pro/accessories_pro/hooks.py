from . import __version__ as app_version

app_name = "accessories_pro"
app_title = "Accessories Pro"
app_publisher = "Your Organization"
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
]

# Installation
# ------------
# before_install = "accessories_pro.install.before_install"
# after_install = "accessories_pro.install.after_install"

# Document Events
# ----------------
# Hook on document methods and events
#
# doc_events = {
# 	"*": {
# 		"on_update": "accessories_pro.utils.on_doc_update"
# 	}
# }

# Scheduled Tasks
# ----------------
scheduler_events = {
	"daily": [
		"accessories_pro.tasks.daily"
	]
}
