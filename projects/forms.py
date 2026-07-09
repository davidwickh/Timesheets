from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "project_name",
            "project_description",
            "start_date",
            "end_date",
            "project_manager",
            "status",
            "total_budget",
            "remaining_budget",
            "budget_spent",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"placeholder": "DD/MM/YYYY"}),
            "end_date": forms.DateInput(attrs={"placeholder": "DD/MM/YYYY"}),
        }
