from django.test import TestCase

from .forms import EmployeeForm
from .models import Employee, Skills


class EmployeeFormTest(TestCase):
    def setUp(self):
        self.skill = Skills.objects.create(skill_name="Python")

    def test_valid_form(self):
        form_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "career_level": "Senior",
            "team": "Engineering",
            "skills": [self.skill.id],
        }
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_form_missing_required_field(self):
        form_data = {
            "first_name": "Jane",
            # last_name is missing
            "email": "jane.doe@example.com",
            "career_level": "Senior",
            "team": "Engineering",
            "skills": [self.skill.id],
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

    def test_invalid_form_bad_email(self):
        form_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "not-an-email",
            "career_level": "Senior",
            "team": "Engineering",
            "skills": [self.skill.id],
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_save_creates_employee(self):
        form_data = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com",
            "career_level": "Junior",
            "team": "Data",
            "skills": [self.skill.id],
        }
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        employee = form.save()
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(employee.first_name, "John")
        self.assertEqual(employee.last_name, "Smith")

    def test_id_field_excluded(self):
        form = EmployeeForm()
        self.assertNotIn("id", form.fields)
