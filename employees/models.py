from random import randint

from django.db import models


class Employee(models.Model):
    # Generate the id by lowering the case of the first and last name and concatenating them
    id = models.CharField(primary_key=True, unique=True, editable=False, max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    career_level = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    # An employee can have multiple skills
    skills = models.ManyToManyField("Skills")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        """Override the save method to generate the id if it does not exist."""
        if not self.id:
            self.id = f"{self.first_name.lower()}_{self.last_name.lower()}"
            # if the id already exists, add a random number to the end
            if Employee.objects.filter(id=self.id).exists():
                self.id = f"{self.id}_{randint(1, 100)}"
        super(Employee, self).save(*args, **kwargs)


class Skills(models.Model):
    id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=100)
