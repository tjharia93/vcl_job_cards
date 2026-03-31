import frappe
from frappe.model.document import Document


class Dies(Document):
	"""
	Dies DocType for managing printing die specifications.

	This DocType stores master data for printing dies including dimensions,
	printing configuration, material specifications, and quantity information.
	Used for auto-populating label specifications in Customer Product Specification.
	"""

	def validate(self):
		"""Main validation method called before saving."""
		self.validate_die_number()
		self.validate_dimensions()

	def validate_die_number(self):
		"""Ensure die number is positive and unique."""
		if self.die_number and self.die_number <= 0:
			frappe.throw("Die Number must be a positive integer.")

	def validate_dimensions(self):
		"""Validate that length and width are positive values."""
		if self.length and self.length <= 0:
			frappe.throw("Length must be greater than zero.")

		if self.width and self.width <= 0:
			frappe.throw("Width must be greater than zero.")
