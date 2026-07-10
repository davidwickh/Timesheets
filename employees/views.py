from django.http import HttpResponse
from django.template import loader
from django.forms.models import model_to_dict

from .forms import EmployeeForm
from .models import Employee


# Create your views here.

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
    """
    if request.method == "GET":
        form = EmployeeForm()
        template = loader.get_template("employees/add_employee_get.html")
        context = {"form": form}
        return HttpResponse(template.render(context, request))

    elif request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            template = loader.get_template("employees/add_employee_post.html")
            return HttpResponse(template.render({}, request))
        template = loader.get_template("employees/add_employee_get.html")
        context = {"form": form}
        return HttpResponse(template.render(context, request))


def detail(request, employee_id: str):
    """Returns all details of an employee from the employees.Models."""
    # Extract all the data from the employee model with the given employee_id
    employee = model_to_dict(Employee.objects.get(id=employee_id))
    for field, value in employee.items():
        print(f"field name: {field}")
        print(f"field value: {value}")
    template = loader.get_template("employees/detail.html")
    context = {"single_employee_data": employee}
    return HttpResponse(template.render(context, request))
