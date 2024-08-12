# Create your views here.

from django.http import HttpResponse
from django.template import loader

from .models import Project
from employees.models import Employee
from datetime import datetime


def detail(request, project_id):
    """Returns all details of a project."""
    return HttpResponse(f"You're looking at project {project_id}")


def index(request):
    """Returns all projects."""
    template = loader.get_template("projects/index.html")
    all_projects = Project.objects.all()
    context = {
        "all_projects": all_projects,
    }
    return HttpResponse(template.render(context, request))


def add_project(request):
    """Two methods, GET and POST. If GET request, render the form to add a new project. If POST request, create a new
    project by adding to the database."""
    if request.method == "GET":
        # Get all fields that are not foreign keys and primary keys
        all_project_fields = []
        for field in Project._meta.fields:
            if not field.primary_key and not field.is_relation:
                if field.name == "start_date" or field.name == "end_date":
                    field.help_text = "Enter the start date in the format DD/MM/YYYY"
                all_project_fields.append(field)
        all_foreign_keys = [field for field in Project._meta.fields if field.is_relation]
        # Convert foreign keys to a dictionary of key-value pairs with the key being the field name and the value being
        # the values from the foreign key table
        foreign_keys_dict = {}
        for fk in all_foreign_keys:
            fk_name = fk.name
            fk_values = fk.related_model.objects.all()
            foreign_keys_dict[fk_name] = [fk_value for fk_value in fk_values]

        template = loader.get_template("projects/add_project_get.html")
        context = {
            "all_fields": all_project_fields,
            "foreign_key_fields": foreign_keys_dict,
        }
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        # Extract the form data
        project_table_fields = [field.name for field in Project._meta.fields if not field.is_relation]
        project_data = {}
        for field in project_table_fields:
            try:
                project_data[field] = request.POST[field]
            except KeyError:
                continue

        # Extract out any foreign key fields
        foreign_key_fields = [field.name for field in Project._meta.fields if field.is_relation]
        for fk_field in foreign_key_fields:
            try:
                # Get the foreign key object
                foreign_key_value = request.POST[fk_field]
                # Get the related model
                related_model = Project._meta.get_field(fk_field).related_model
                # Get the related object
                related_object = related_model.objects.get(id=foreign_key_value)
            except KeyError:
                continue

        # Convert the start_date and end_date to a datetime object
        try:
            project_data["start_date"] = datetime.strptime(project_data["start_date"], "%d/%m/%Y")
            project_data["end_date"] = datetime.strptime(project_data["end_date"], "%d/%m/%Y")
        except ValueError:
            return HttpResponse("Invalid date format. Please enter the date in the format DD/MM/YYYY")

        # Create a new project
        new_project = Project(**project_data)
        # Save the project to the database
        new_project.save()
        # Redirect to the index page
        return HttpResponse("Project added successfully. <a href='/projects/'>Go back to the projects page</a>")
