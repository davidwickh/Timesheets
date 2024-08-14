"""This module contains the database models for the employees app."""

# pylint: disable=too-few-public-methods
from random import randint

from django.db import models


class Employee(models.Model):
    """Model for an employee in the company."""

    # Generate the id by lowering the case of the first and last name and concatenating them
    id = models.CharField(primary_key=True, unique=True, editable=False, max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    career_level = models.CharField(max_length=100)
    team = models.ForeignKey("Teams", on_delete=models.CASCADE)
    # An employee can have multiple skills
    skills = models.ManyToManyField("Skills")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """
        Override the save method to generate the id if it does not exist. Can handle duplicate ids.
        """
        if not self.id:
            self.id = f"{str(self.first_name).lower()}_{str(self.last_name).lower()}"
            # if the id already exists, add a random number to the end
            if Employee.objects.filter(id=self.id).exists():
                self.id = f"{self.id}_{randint(1, 100)}"
        # pylint: disable=super-with-arguments
        super(Employee, self).save(*args, **kwargs)


class Skills(models.Model):
    """Model for the skills an employee can have."""

    skill_name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.skill_name


class Teams(models.Model):
    """Model for the teams in the company that an employee would belong to."""

    team_name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.team_name
