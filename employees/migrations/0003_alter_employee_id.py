# Generated by Django 5.1a1 on 2024-06-12 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_alter_employee_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.CharField(editable=False, max_length=200, primary_key=True, serialize=False, unique=True),
        ),
    ]
