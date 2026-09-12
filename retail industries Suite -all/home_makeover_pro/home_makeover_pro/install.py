# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe


def before_install():
	make_custom_fields()


def after_uninstall():
	delete_custom_fields()


def make_custom_fields():
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	create_custom_fields(
		{
			"Sales Invoice": [
				dict(
					fieldname="home_makeover_milestone_payment",
					label="Home Makeover Milestone Payment",
					fieldtype="Link",
					options="Project Milestone Payment",
					insert_after="customer",
					print_hide=1,
					no_copy=1,
				)
			]
		},
		ignore_validate=True,
	)


def delete_custom_fields():
	from frappe.custom.doctype.custom_field.custom_field import delete_custom_fields

	delete_custom_fields(
		{"Sales Invoice": ["home_makeover_milestone_payment"]}
	)
