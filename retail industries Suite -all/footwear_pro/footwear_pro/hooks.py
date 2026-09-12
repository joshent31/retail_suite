from . import __version__ as app_version

app_name = "footwear_pro"
app_title = "Footwear Pro"
app_publisher = "Your Organization"
app_description = "Style masters, size runs, material BOM, QC, warranty claims and vendor ratings for footwear retail on ERPNext."
app_email = "admin@example.com"
app_license = "MIT"
required_apps = ["frappe/erpnext"]

# Includes in <head>
# ------------------
# app_include_css = "/assets/footwear_pro/css/footwear_pro.css"
# app_include_js = "/assets/footwear_pro/js/footwear_pro.js"

# Fixtures
# --------
# Exported as data via `bench --site [site] export-fixtures`
fixtures = [
	{"dt": "Role", "filters": [["name", "in", ['Footwear Manager', 'Footwear User']]]},
	{"dt": "Notification", "filters": [["module", "=", "Footwear Management"]]},
	{"dt": "Workflow", "filters": [["document_type", "in", ['Footwear Warranty Claim']]]},
	{"dt": "Print Format", "filters": [["module", "=", "Footwear Management"]]},
]

# Installation
# ------------
# before_install = "footwear_pro.install.before_install"
# after_install = "footwear_pro.install.after_install"

# Document Events
# ----------------
# Hook on document methods and events
#
# doc_events = {
# 	"*": {
# 		"on_update": "footwear_pro.utils.on_doc_update"
# 	}
# }

# Scheduled Tasks
# ----------------
scheduler_events = {
	"daily": [
		"footwear_pro.tasks.daily"
	]
}
