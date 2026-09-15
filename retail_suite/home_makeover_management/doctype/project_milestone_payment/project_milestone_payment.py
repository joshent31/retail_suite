# Copyright (c) 2026, Your Organization and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ProjectMilestonePayment(Document):
	def validate(self):
		self.validate_milestones()
		self.validate_against_budget()

	def validate_milestones(self):
		if not self.milestones:
			frappe.throw(_("At least one milestone is required"))
		total_percent = sum(flt(m.percentage) for m in self.milestones)
		if total_percent > 100:
			frappe.throw(
				_("Total milestone percentage cannot exceed 100% (currently {0}%)").format(
					total_percent
				)
			)

	def validate_against_budget(self):
		if not self.project:
			return
		project_budget = frappe.db.get_value(
			"Home Makeover Project", self.project, "budget_estimate"
		)
		if not project_budget:
			return

		existing_docs = frappe.get_all(
			"Project Milestone Payment",
			filters={
				"project": self.project,
				"docstatus": 1,
				"name": ["!=", self.name or ""],
			},
			pluck="name",
		)
		already = 0
		if existing_docs:
			already = frappe.db.sql(
				"""SELECT COALESCE(SUM(amount), 0)
				   FROM `tabProject Milestone Detail`
				   WHERE parent IN %s AND parenttype = 'Project Milestone Payment'""",
				(tuple(existing_docs),),
			)[0][0] or 0

		new_total = flt(already) + sum(flt(m.amount) for m in self.milestones)
		if new_total > flt(project_budget):
			frappe.throw(
				_("Milestone total ({0}) would exceed the project budget ({1})").format(
					frappe.utils.fmt_money(new_total),
					frappe.utils.fmt_money(project_budget),
				)
			)


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	"""Create a draft Sales Invoice from the Pending milestones of a submitted Milestone Payment doc."""
	frappe.only_for(("Home Makeover Manager", "System Manager"))

	source = frappe.get_doc("Project Milestone Payment", source_name)
	if source.docstatus != 1:
		frappe.throw(_("Only submitted Milestone Payment documents can be invoiced"))

	billing_item = source.billing_item or frappe.db.get_single_value(
		"Home Makeover Settings", "default_billing_item"
	)
	if not billing_item:
		frappe.throw(_("Set a Billing Item on the document or in Home Makeover Settings"))

	pending = [m for m in source.milestones if m.status == "Pending"]
	if not pending:
		frappe.throw(_("No Pending milestones left to invoice"))

	invoice = frappe.new_doc("Sales Invoice")
	invoice.customer = frappe.db.get_value(
		"Home Makeover Project", source.project, "customer"
	)
	invoice.home_makeover_milestone_payment = source.name

	for m in pending:
		invoice.append(
			"items",
			{
				"item_code": billing_item,
				"item_name": _("Milestone: {0}").format(m.milestone_name),
				"qty": 1,
				"rate": flt(m.amount),
				"description": _("{0} - milestone {1} for project {2}").format(
					m.milestone_name, m.idx, source.project
				),
			},
		)

	invoice.set_missing_values()
	invoice.calculate_taxes_and_totals()
	invoice.insert(ignore_permissions=True)

	for m in pending:
		m.db_set("status", "Invoiced")
	frappe.db.set_value(
		"Project Milestone Payment", source.name, "latest_invoice", invoice.name
	)

	frappe.msgprint(_("Sales Invoice {0} created").format(frappe.bold(invoice.name)))
	return invoice.name
