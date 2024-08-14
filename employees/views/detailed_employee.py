"""
Visual aspects for viewing a specific employees details and updating them
"""

from django.urls import reverse_lazy
from django.views.generic import UpdateView

from employees.models import Employee


class DetailedEmployeeView(UpdateView):
    """View for viewing and updating a specific employee's details."""

    model = Employee
    fields = "__all__"
    template_name = "employees/detail.html"
    context_object_name = "employee"

    def get_object(self):
        """Get the specific employee object from request URL."""
        return Employee.objects.get(id=self.kwargs["employee_id"])

    def get_success_url(self):
        """Redirect to the index page after updating an employee."""
        return reverse_lazy("employees:index")  # Correctly references the namespace
