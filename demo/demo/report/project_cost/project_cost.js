// Copyright (c) 2022, niyaz and contributors
// For license information, please see license.txt

frappe.query_reports["Project Cost"] = {
	"filters": [
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"reqd": 1
		}
	]
};
