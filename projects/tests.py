from django.test import TestCase

from employees.models import Employee, Skills
from .forms import ProjectForm
from .models import Project


class ProjectFormTest(TestCase):
    def setUp(self):
        skill = Skills.objects.create(skill_name="Python")
        self.manager = Employee.objects.create(
            first_name="Alice",
            last_name="Manager",
            email="alice@example.com",
            career_level="Principal",
            team="Engineering",
        )

    def test_valid_form(self):
        form_data = {
            "project_name": "Test Project",
            "project_description": "A test project",
            "start_date": "2024-01-01",
            "end_date": "2024-06-30",
            "project_manager": self.manager.id,
            "status": "Bid",
            "total_budget": "100000.00",
            "remaining_budget": "100000.00",
            "budget_spent": "0.00",
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_form_missing_required_field(self):
        form_data = {
            # project_name is missing
            "project_description": "A test project",
            "start_date": "2024-01-01",
            "end_date": "2024-06-30",
            "project_manager": self.manager.id,
            "status": "Bid",
            "total_budget": "100000.00",
            "remaining_budget": "100000.00",
            "budget_spent": "0.00",
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("project_name", form.errors)

    def test_invalid_form_bad_status(self):
        form_data = {
            "project_name": "Test Project",
            "project_description": "A test project",
            "start_date": "2024-01-01",
            "end_date": "2024-06-30",
            "project_manager": self.manager.id,
            "status": "InvalidStatus",
            "total_budget": "100000.00",
            "remaining_budget": "100000.00",
            "budget_spent": "0.00",
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("status", form.errors)

    def test_form_save_creates_project(self):
        form_data = {
            "project_name": "New Project",
            "project_description": "Description here",
            "start_date": "2024-03-01",
            "end_date": "2024-12-31",
            "project_manager": self.manager.id,
            "status": "In Progress",
            "total_budget": "50000.00",
            "remaining_budget": "45000.00",
            "budget_spent": "5000.00",
        }
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        project = form.save()
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(project.project_name, "New Project")

    def test_id_field_excluded(self):
        form = ProjectForm()
        self.assertNotIn("id", form.fields)
