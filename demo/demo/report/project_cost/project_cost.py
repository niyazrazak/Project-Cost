# Copyright (c) 2022, niyaz and contributors
# For license information, please see license.txt

import json

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = []
	amount = frappe.db.get_all("Payment Entry", filters=conditions, fields=[
		"posting_date", "payment_type", "paid_amount as payment_received"
	])
	for amt in amount:
		if amt.get("payment_type") == 'Receive':
			data.append(amt)

	materials = frappe.db.get_all("Stock Entry", filters=conditions, 
		or_filters={"purpose":"Material Issue"}, fields=[
		"posting_date", "sum(total_amount) as materials"
	])
	for mat in materials:
		data.append(mat)

	labour = frappe.db.get_all("Timesheet Detail", filters=conditions, fields=[
		'sum(billing_amount) as labour'
	])
	for lab in labour:
		data.append(lab)

	other_expense = frappe.db.sql(
		"""
		select
			`tabPurchase Invoice`.posting_date, sum(`tabPurchase Invoice Item`.`amount`) as other_expense
		from `tabPurchase Invoice`, `tabPurchase Invoice Item`
		where `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.`parent` and
		`tabPurchase Invoice`.docstatus = 1
	""",as_dict=1)
	
	for exp in other_expense:
		data.append(exp)
	# other_expense = frappe.db.get_all("Purchase Invoice Item", filters=conditions, fields=[
	# 	"DATE(creation) as posting_date", 'sum(amount) as other_expense'
	# ])
	# frappe.msgprint(str(other_expense))
	return columns, data

def get_conditions(filters):
	if not isinstance(filters, dict):
		filters = json.loads(filters)

	conditions = {}
	if filters.project:
		conditions["project"] = filters.project
	
	conditions["docstatus"] = 1
	
	return conditions


def get_columns(filters):
	columns = [
		{
			"label": _("Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Payment Received"),
			"fieldname": "payment_received",
			"fieldtype": "Data",
		},
		{
			"label": _("Materials"),
			"fieldname": "materials",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Labour"),
			"fieldname": "labour",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Subcon"),
			"fieldname": "subcon",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Other Expense"),
			"fieldname": "other_expense",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Ptt Cash"),
			"fieldname": "subcon",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Po/bilss"),
			"fieldname": "subcon",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Pending"),
			"fieldname": "subcon",
			"fieldtype": "Data",
			"width": 100
		},
	]

	return columns
