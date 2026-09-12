# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe


def before_install():
	make_custom_fields()


def after_uninstall():
	delete_custom_fields()


def make_custom_fields():
	"""Add quiet app-specific link fields to core doctypes for traceability."""
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	create_custom_fields(
		{
			"Stock Entry": [
				dict(
					fieldname="apparel_pro_production_order",
					label="Apparel Production Order",
					fieldtype="Link",
					options="Apparel Production Order",
					insert_after="stock_entry_type",
					print_hide=1,
					no_copy=1,
				)
			],
			"Sales Invoice Item": [
				dict(
					fieldname="apparel_style",
					label="Apparel Style",
					fieldtype="Link",
					options="Apparel Style Master",
					insert_after="item_code",
					fetch_from="item_code.apparel_style",
					print_hide=1,
					no_copy=1,
				)
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
		}
	)
