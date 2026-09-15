# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt


def before_install():
	make_custom_fields()


def after_uninstall():
	delete_custom_fields()


def make_custom_fields():
	"""App-specific link fields on core doctypes, per sector, for traceability."""
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	create_custom_fields(
		{
			"Stock Entry": [
				{
					"fieldname": "apparel_pro_production_order",
					"label": "Apparel Production Order",
					"fieldtype": "Link",
					"options": "Apparel Production Order",
					"insert_after": "stock_entry_type",
					"print_hide": 1,
					"no_copy": 1,
				}
			],
			"Sales Invoice Item": [
				{
					"fieldname": "apparel_style",
					"label": "Apparel Style",
					"fieldtype": "Link",
					"options": "Apparel Style Master",
					"insert_after": "item_code",
					"fetch_from": "item_code.apparel_style",
					"print_hide": 1,
					"no_copy": 1,
				}
			],
			"Purchase Invoice": [
				{
					"fieldname": "accessories_consignment_stock",
					"label": "Accessories Consignment Stock",
					"fieldtype": "Link",
					"options": "Accessory Consignment Stock",
					"insert_after": "supplier",
					"print_hide": 1,
					"no_copy": 1,
				}
			],
			"Sales Invoice": [
				{
					"fieldname": "home_makeover_milestone_payment",
					"label": "Home Makeover Milestone Payment",
					"fieldtype": "Link",
					"options": "Project Milestone Payment",
					"insert_after": "customer",
					"print_hide": 1,
					"no_copy": 1,
				}
			],
		},
		ignore_validate=True,
	)


def delete_custom_fields():
	from frappe.custom.doctype.custom_field.custom_field import delete_custom_fields

	delete_custom_fields(
		{
			"Stock Entry": ["apparel_pro_production_order"],
			"Sales Invoice Item": ["apparel_style"],
			"Purchase Invoice": ["accessories_consignment_stock"],
			"Sales Invoice": ["home_makeover_milestone_payment"],
		}
	)
