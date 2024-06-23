#!/usr/bin/env zsh

# drop the database
sudo rm -f db.sqlite3
# loop through all migrations and delete them
for migration in $(find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./venv/*"); do
    sudo rm -f $migration
done
# Create a new migration
python manage.py makemigrations
# Apply the migration
python manage.py migrate
