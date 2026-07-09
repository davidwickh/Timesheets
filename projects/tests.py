from django.test import TestCase

from employees.models import Employee
from .forms import ProjectForm
from .models import Project


class ProjectFormTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="Manager",
            last_name="Test",
            email="manager@example.com",
            career_level="Senior",
            team="Management",
        )

    def test_form_has_correct_fields(self):
        form = ProjectForm()
        expected_fields = [
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
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_valid_form(self):
        data = {
            "project_name": "Test Project",
            "project_description": "A test project",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "project_manager": self.employee.id,
            "status": "Bid",
            "total_budget": "10000.00",
            "remaining_budget": "8000.00",
            "budget_spent": "2000.00",
        }
        form = ProjectForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_required_field(self):
        data = {
            "project_name": "",
            "project_description": "A test project",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "project_manager": self.employee.id,
            "status": "Bid",
            "total_budget": "10000.00",
            "remaining_budget": "8000.00",
            "budget_spent": "2000.00",
        }
        form = ProjectForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_status_choice(self):
        data = {
            "project_name": "Test Project",
            "project_description": "A test project",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "project_manager": self.employee.id,
            "status": "Invalid Status",
            "total_budget": "10000.00",
            "remaining_budget": "8000.00",
            "budget_spent": "2000.00",
        }
        form = ProjectForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_save_creates_project(self):
        data = {
            "project_name": "New Project",
            "project_description": "New project description",
            "start_date": "2024-06-01",
            "end_date": "2024-12-31",
            "project_manager": self.employee.id,
            "status": "In Progress",
            "total_budget": "50000.00",
            "remaining_budget": "40000.00",
            "budget_spent": "10000.00",
        }
        form = ProjectForm(data=data)
        self.assertTrue(form.is_valid())
        project = form.save()
        self.assertEqual(project.project_name, "New Project")
        self.assertEqual(project.project_manager, self.employee)


class AddProjectViewTest(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create(
            first_name="Manager",
            last_name="Test",
            email="manager@example.com",
            career_level="Senior",
            team="Management",
        )

    def test_get_renders_form(self):
        response = self.client.get("/projects/add_project/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add Project", response.content)
        self.assertIn(b"project_name", response.content)

    def test_post_valid_data_creates_project(self):
        data = {
            "project_name": "View Test Project",
            "project_description": "Created from view test",
            "start_date": "2024-03-01",
            "end_date": "2024-09-30",
            "project_manager": self.employee.id,
            "status": "Bid",
            "total_budget": "20000.00",
            "remaining_budget": "20000.00",
            "budget_spent": "0.00",
        }
        response = self.client.post("/projects/add_project/", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Project.objects.filter(project_name="View Test Project").exists())

    def test_post_invalid_data_shows_form_with_errors(self):
        data = {
            "project_name": "",
            "project_description": "Missing name",
            "start_date": "2024-03-01",
            "end_date": "2024-09-30",
            "project_manager": self.employee.id,
            "status": "Bid",
            "total_budget": "20000.00",
            "remaining_budget": "20000.00",
            "budget_spent": "0.00",
        }
        response = self.client.post("/projects/add_project/", data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.exists())
