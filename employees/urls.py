"""Contains the URL patterns for the employees app."""

from django.urls import path

from .views.add_employee import AddEmployeeView
from .views.all_employees import AllEmployeesView
from .views.detailed_employee import DetailedEmployeeView

APP_NAME = "employees"
urlpatterns = [
    # ex: /employees/
    path("", AllEmployeesView.as_view(), name="index"),
    # Add employee, Can be either a GET or POST request
    path("add/", AddEmployeeView.as_view(), name="add"),
    # ex: /employees/david_wickham/detail
    path("<str:employee_id>/detail/", DetailedEmployeeView.as_view(), name="detail"),
]
