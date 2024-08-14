"""
Visual components for adding an employee to the database.
"""

# pylint: disable=too-few-public-methods
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView

from employees.models import Employee, Skills


class AddEmployeeForm(forms.ModelForm):
    """Dummy form for adding an employee, for POST validation process."""

    skills = forms.ModelMultipleChoiceField(
        queryset=Skills.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        """Meta class for the AddEmployeeForm."""

        model = Employee
        fields = "__all__"


class AddEmployeeView(CreateView):
    """View for adding an employee."""

    model = Employee
    form_class = AddEmployeeForm
    template_name = "employees/add.html"
    success_url = reverse_lazy(
        "employees:index"
    )  # Redirect to the index page after adding an employee
