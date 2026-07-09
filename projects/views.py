# Create your views here.

from django.http import HttpResponse
from django.template import loader

from .forms import ProjectForm
from .models import Project


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
        form = ProjectForm()
        template = loader.get_template("projects/add_project_get.html")
        context = {"form": form}
        return HttpResponse(template.render(context, request))
    elif request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            template = loader.get_template("projects/add_project_post.html")
            return HttpResponse(template.render({}, request))
        else:
            template = loader.get_template("projects/add_project_get.html")
            context = {"form": form}
            return HttpResponse(template.render(context, request))
