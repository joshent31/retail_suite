from . import __version__ as app_version

app_name = "lifestyle_fashion_pro"
app_title = "Lifestyle & Fashion Pro"
app_publisher = "Your Organization"
app_description = "Collections, influencer collaborations, trend boards, lookbooks, loyalty points and style consultations for lifestyle/fashion retail on ERPNext."
app_email = "admin@example.com"
app_license = "MIT"
required_apps = ["frappe/erpnext"]

# Includes in <head>
# ------------------
# app_include_css = "/assets/lifestyle_fashion_pro/css/lifestyle_fashion_pro.css"
# app_include_js = "/assets/lifestyle_fashion_pro/js/lifestyle_fashion_pro.js"

# Fixtures
# --------
# Exported as data via `bench --site [site] export-fixtures`
fixtures = [
	{"dt": "Role", "filters": [["name", "in", ['Fashion Manager', 'Fashion Stylist']]]},
	{"dt": "Notification", "filters": [["module", "=", "Lifestyle Fashion Management"]]},
	{"dt": "Workflow", "filters": [["document_type", "in", ['Influencer Brand Collaboration']]]},
	{"dt": "Print Format", "filters": [["module", "=", "Lifestyle Fashion Management"]]},
]

# Installation
# ------------
# before_install = "lifestyle_fashion_pro.install.before_install"
# after_install = "lifestyle_fashion_pro.install.after_install"

# Document Events
# ----------------
# Hook on document methods and events
#
# doc_events = {
# 	"*": {
# 		"on_update": "lifestyle_fashion_pro.utils.on_doc_update"
# 	}
# }

# Scheduled Tasks
# ----------------
scheduler_events = {
	"daily": [
		"lifestyle_fashion_pro.tasks.daily"
	]
}
