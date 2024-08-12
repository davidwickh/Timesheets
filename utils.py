
from datetime import datetime
from django.db.models import Model


class DataFormatter:
    """Class to take Django values going from the UI to the database for correct type formatting, and
    from the database to the UI for human readable formatting."""

    def __init__(self):
        self.ui_date_format = "%d/%m/%Y"
        self.database_date_format = "%Y-%m-%d"

    def from_ui_to_database(self, data: Model._meta.fields):
