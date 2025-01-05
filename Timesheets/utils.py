from typing import Any, Optional

from django.db import models


def get_model_values_and_foreign_key_values(
    model: models.Model,
    fields_to_exclude: Optional[list[str]] = None,
) -> dict[str, list[Any] | dict[Any, list[Any]]]:
    """
    Helper function to take a django model and return a dictionary of context with all model keys and all foreign keys
    with their values.
    :param model: The django model to create an input form from
    :param fields_to_exclude: A list of fields to exclude from the input form
    :return: A dictionary of context with all model keys and all foreign keys with their values
    """
    all_project_fields = []

    for field in model._meta.fields:
        if field.primary_key or field.is_relation or field.name in fields_to_exclude:
            continue
        else:
            all_project_fields.append(field)

        all_foreign_keys = [field for field in model._meta.fields if
                            field.is_relation and field.name not in fields_to_exclude]
        # Convert foreign keys to a dictionary of key-value pairs with the key being the field name and the value being
        # the values from the foreign key table
        foreign_keys_dict = {}
        for fk in all_foreign_keys:
            fk_name = fk.name
            fk_values = fk.related_model.objects.all()
            foreign_keys_dict[fk_name] = [fk_value for fk_value in fk_values]

        return {
            "all_fields": all_project_fields,
            "foreign_key_fields": foreign_keys_dict,
        }
