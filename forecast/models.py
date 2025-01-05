from django.db import models
from projects.models import Project


class InWeekForcast(models.Model):
    """Model to store the forecasted hours, taken from the reference week, and projected out x weeks into the future
    as defined by weeks_out"""
    employee_id = models.CharField(max_length=200)
    week_ending = models.DateField()
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    weeks_out = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id} - {self.week_ending} - {self.project_id} - {self.hours} - {self.weeks_out}"
