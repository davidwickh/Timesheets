from django.http import HttpResponse
from django.template import loader

from .models import Employee


# Create your views here.

def detail(request, employee_id):
    """Returns all details of an employee."""
    return HttpResponse(f"You're looking at employee {employee_id}")


def index(request):
    """Returns all employees."""
    all_employees = Employee.objects.all()
    template = loader.get_template("employees/index.html")
    context = {
        "all_employees": all_employees,
    }
    return HttpResponse(template.render(context, request))


def add_employee(request):
    """
    Add employee view. If GET request, render the form to add a new employee. If POST request, create a new employee
    by adding to the database.
    :param request:
    :return:
    """
    if request.method == "GET":
        # Get all the fields from the Employee model
        all_fields = Employee._meta.fields
        all_fields = all_fields[1:]
        # Render the form
        template = loader.get_template("employees/add_employee_get.html")
        context = {
            "foreign_key_fields": {},  # No foreign keys in the Employee model
            "all_fields": all_fields,
        }
        return HttpResponse(template.render(context, request))

    elif request.method == "POST":
        # Get the form data
        employee_fields = [field.name for field in Employee._meta.fields]
        form_data = {}
        for field in employee_fields:
            try:
                form_data[field] = request.POST[field]
            except KeyError:
                continue
        # Create a new employee
        new_employee = Employee(**form_data)
        # Save the employee to the database
        new_employee.save()
        # Redirect to the index page
        return HttpResponse("Employee added successfully. <a href='/employees/'>Go back to the employees page</a>")


def projects(request, employee_id):
    """Returns all projects that employee is currently working on."""
    return HttpResponse("You're looking at all projects.")
