from django.urls import path

from . import views

urlpatterns = [
    # ex: /employees/
    path("", views.index, name="index"),
    # ex: /employees/5/
    path("<int:employee_id>/", views.detail, name="detail"),
    # Add employee, Can be either a GET or POST request
    path("add_employee/", views.add_employee, name="add_employee"),
]
