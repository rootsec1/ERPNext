# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.model.document import Document
from frappe.utils import cint


class BuyingSettings(Document):
	def on_update(self):
		# Custom price list
		if not self.buying_price_list:
			self.buying_price_list = "Indian"
			self.save()
		self.toggle_discount_accounting_fields()

	def validate(self):
		for key in ["supplier_group", "supp_master_name", "maintain_same_rate"]:
			frappe.db.set_default(key, self.get(key, ""))
		
		# Custom price list
		if not frappe.db.get_default("buying_price_list"):
			frappe.db.set_default("buying_price_list", self.get("buying_price_list", "Indian"))

		from erpnext.setup.doctype.naming_series.naming_series import set_by_naming_series

		set_by_naming_series(
			"Supplier",
			"supplier_name",
			self.get("supp_master_name") == "Naming Series",
			hide_name_field=False,
		)

	def toggle_discount_accounting_fields(self):
		enable_discount_accounting = cint(self.enable_discount_accounting)

		make_property_setter(
			"Purchase Invoice Item",
			"discount_account",
			"hidden",
			not (enable_discount_accounting),
			"Check",
			validate_fields_for_doctype=False,
		)
		if enable_discount_accounting:
			make_property_setter(
				"Purchase Invoice Item",
				"discount_account",
				"mandatory_depends_on",
				"eval: doc.discount_amount",
				"Code",
				validate_fields_for_doctype=False,
			)
		else:
			make_property_setter(
				"Purchase Invoice Item",
				"discount_account",
				"mandatory_depends_on",
				"",
				"Code",
				validate_fields_for_doctype=False,
			)

		make_property_setter(
			"Purchase Invoice",
			"additional_discount_account",
			"hidden",
			not (enable_discount_accounting),
			"Check",
			validate_fields_for_doctype=False,
		)
		if enable_discount_accounting:
			make_property_setter(
				"Purchase Invoice",
				"additional_discount_account",
				"mandatory_depends_on",
				"eval: doc.discount_amount",
				"Code",
				validate_fields_for_doctype=False,
			)
		else:
			make_property_setter(
				"Purchase Invoice",
				"additional_discount_account",
				"mandatory_depends_on",
				"",
				"Code",
				validate_fields_for_doctype=False,
			)
