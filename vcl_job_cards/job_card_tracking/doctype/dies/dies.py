import frappe
from frappe.model.document import Document


class Dies(Document):
	def validate(self):
		self.validate_die_number()
		self.validate_dimensions()

	def validate_die_number(self):
		"""Ensure die number is positive"""
		if self.die_number and self.die_number <= 0:
			frappe.throw("Die Number must be a positive integer.")

	def validate_dimensions(self):
		"""Validate that length and width are positive"""
		if self.length and self.length <= 0:
			frappe.throw("Length must be greater than zero.")
		
		if self.width and self.width <= 0:
			frappe.throw("Width must be greater than zero.")
