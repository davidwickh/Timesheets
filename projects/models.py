from django.db import models


class Project(models.Model):
    """Model representing a project."""
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    # Employee is in the employees app
    project_manager = models.ForeignKey("employees.Employee", on_delete=models.CASCADE)
    # project_team = models.ManyToManyField("employees.Employee")
    status = models.CharField(
        max_length=100,
        choices=[
            ("Bid", "Bid"),
            ("In Progress", "In Progress"),
            ("Complete", "Complete"),
        ]
    )
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2)
    budget_spent = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.project_name


# class ProjectTeam(models.Model):
#     """A project team model is made up of multiple employees with specific roles and bill rates."""
#     id = models.AutoField(primary_key=True)
#     project_id = models.ForeignKey("Project", on_delete=models.CASCADE)
#     employee_id = models.ForeignKey("employees.Employee", on_delete=models.CASCADE)
#     role = models.CharField(max_length=100)
#     bill_rate = models.DecimalField(max_digits=10, decimal_places=2)
#
#     def __str__(self):
#         return f"{self.project_id} - {self.employee_id}"
