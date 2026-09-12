# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt



def before_install():
	make_custom_fields()


def after_uninstall():
	delete_custom_fields()


def make_custom_fields():
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	create_custom_fields(
		{
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
			]
		},
		ignore_validate=True,
	)


def delete_custom_fields():
	from frappe.custom.doctype.custom_field.custom_field import delete_custom_fields

	delete_custom_fields(
		{"Purchase Invoice": ["accessories_consignment_stock"]}
	)
