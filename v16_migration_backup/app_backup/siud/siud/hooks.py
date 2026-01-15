app_name = "siud"
app_title = "Siud"
app_publisher = "Tzvi"
app_description = "Siud"
app_email = "tzvimg@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "siud",
# 		"logo": "/assets/siud/logo.png",
# 		"title": "Siud",
# 		"route": "/siud",
# 		"has_permission": "siud.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/siud/css/siud.css"
# app_include_js = "/assets/siud/js/siud.js"

# include js, css files in header of web template
# web_include_css = "/assets/siud/css/siud.css"
# web_include_js = "/assets/siud/js/siud.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "siud/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "siud/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
role_home_page = {
	"Supplier Portal User": "supplier-dashboard"
}

# Portal Menu Items
# ------------------
# Standard portal menu items to show in the portal
standard_portal_menu_items = [
	{"title": "דף הבית", "route": "/supplier-dashboard", "reference_doctype": "", "role": "Supplier Portal User"},
	{"title": "הפניות שלי", "route": "/supplier-inquiry-form/list", "reference_doctype": "Supplier Inquiry", "role": "Supplier Portal User"},
	{"title": "פנייה חדשה", "route": "/supplier-inquiry-form/new", "reference_doctype": "Supplier Inquiry", "role": "Supplier Portal User"},
	{"title": "פרופיל הספק", "route": "/supplier-profile", "reference_doctype": "Supplier", "role": "Supplier Portal User"},
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "siud.utils.jinja_methods",
# 	"filters": "siud.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "siud.install.before_install"
# after_install = "siud.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "siud.uninstall.before_uninstall"
# after_uninstall = "siud.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "siud.utils.before_app_install"
# after_app_install = "siud.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "siud.utils.before_app_uninstall"
# after_app_uninstall = "siud.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "siud.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"siud.tasks.all"
# 	],
# 	"daily": [
# 		"siud.tasks.daily"
# 	],
# 	"hourly": [
# 		"siud.tasks.hourly"
# 	],
# 	"weekly": [
# 		"siud.tasks.weekly"
# 	],
# 	"monthly": [
# 		"siud.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "siud.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "siud.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "siud.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "siud.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["siud.utils.before_request"]
# after_request = ["siud.utils.after_request"]

# Job Events
# ----------
# before_job = ["siud.utils.before_job"]
# after_job = ["siud.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"siud.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

