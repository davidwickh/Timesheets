from django.urls import path

from . import views

urlpatterns = [
    # ex: /projects/
    path("", views.index, name="index"),
    # ex: /projects/5/
    path("<int:project_id>/", views.detail, name="detail"),
    # Add project, Can be either a GET or POST request
    path("add_project/", views.add_project, name="add_project"),
]
