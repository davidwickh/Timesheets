from django.test import TestCase, RequestFactory

from .forms import EmployeeForm
from .models import Employee


class EmployeeFormTest(TestCase):
    def test_form_has_correct_fields(self):
        form = EmployeeForm()
        self.assertEqual(
            list(form.fields.keys()),
            ["first_name", "last_name", "email", "career_level", "team"],
        )

    def test_valid_form(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "career_level": "Senior",
            "team": "Engineering",
        }
        form = EmployeeForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_required_field(self):
        data = {
            "first_name": "John",
            "last_name": "",
            "email": "john.doe@example.com",
            "career_level": "Senior",
            "team": "Engineering",
        }
        form = EmployeeForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_bad_email(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "not-an-email",
            "career_level": "Senior",
            "team": "Engineering",
        }
        form = EmployeeForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_save_creates_employee(self):
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "career_level": "Junior",
            "team": "Design",
        }
        form = EmployeeForm(data=data)
        self.assertTrue(form.is_valid())
        employee = form.save()
        self.assertEqual(employee.first_name, "Jane")
        self.assertEqual(employee.last_name, "Smith")
        self.assertEqual(employee.id, "jane_smith")


class AddEmployeeViewTest(TestCase):
    def test_get_renders_form(self):
        response = self.client.get("/employees/add_employee/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add Employee", response.content)
        self.assertIn(b"first_name", response.content)

    def test_post_valid_data_creates_employee(self):
        data = {
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice@example.com",
            "career_level": "Mid",
            "team": "Product",
        }
        response = self.client.post("/employees/add_employee/", data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Employee.objects.filter(id="alice_wonder").exists())

    def test_post_invalid_data_shows_form_with_errors(self):
        data = {
            "first_name": "Bob",
            "last_name": "",
            "email": "bob@example.com",
            "career_level": "Senior",
            "team": "Engineering",
        }
        response = self.client.post("/employees/add_employee/", data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Employee.objects.filter(first_name="Bob").exists())
