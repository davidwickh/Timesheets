"""
Visual aspects of the application that relate to creating a view of all employees in a table format.
"""

# pylint: disable=too-few-public-methods
from django.views.generic import ListView

from employees.models import Employee


class AllEmployeesView(ListView):
    """View for returning all employees in a table format."""

    model = Employee
    template_name = "employees/index.html"
    context_object_name = "employees"
    http_method_names = ["get"]

    def get_queryset(self):
        """Creates a table of all employees."""
        return Employee.objects.values("id", "first_name", "last_name", "email", "team")
