import os

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework import exceptions

PhoneNumberValidator = RegexValidator(r"^0[0-9]{10,12}$", "Invalid Phone Number")


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [
        ".pdf",
        ".doc",
        ".docx",
        ".jpg",
        ".png",
        ".xlsx",
        ".xls",
        ".ppt",
    ]
    if ext.lower() not in valid_extensions:
        raise ValidationError("Unsupported file extension.")


PhoneNumberValidator = RegexValidator(r"^0[0-9]{10,12}$", "Invalid Phone Number")

ZipCodeValidator = RegexValidator("^(^[0-9]{5}(?:-[0-9]{4})?$|^$)", "Invalid ZIP Code")


def validate_phone_number_length(value):
    if len(value) < 9:
        raise ValidationError("Phone number should be at least 9 digits")
    else:
        return value


def validate_file_size(value):
    filesize = value.size

    if filesize > 3 * 1024 * 1024:
        raise exceptions.ValidationError("Max file size is 3 Mb")
    else:
        return value
