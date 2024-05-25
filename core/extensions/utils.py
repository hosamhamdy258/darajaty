import itertools
import random
import string
import time
from collections import Counter
from io import BytesIO
from typing import Any, Dict, List, Optional

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.files import File
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# from django_countries.serializers import CountryFieldMixin
from hashid_field import HashidAutoField, HashidField
from hashid_field.rest import HashidSerializerCharField
from PIL import Image
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import exceptions, serializers
from rest_framework.pagination import PageNumberPagination


def duplicated_value_checker(iterable: List[Dict[str, Any]], keys: Dict[str, Optional[Any]]):
    """
    Checks for duplicate values in the given iterable of dicts based on specified keys.

    Args:
        iterable (Iterable[Dict[str, Any]]): An iterable of dictionaries to check for duplicates.
        keys (Dict[str, Any]): A dictionary where the keys are the fields to check for duplicates,
                               and the values are specific values to check against (or None to check any value).

    Raises:
        serializers.ValidationError: If duplicate values are found.
    """

    values_to_check = [(key, dict_item[key]) for dict_item in iterable for key in dict_item if key in keys]

    value_counts = Counter(values_to_check)

    duplicated_keys = [key for (key, value), count in value_counts.items() if count > 1 and (keys[key] is None or value == keys[key])]

    if duplicated_keys:
        raise serializers.ValidationError({"error": f"{duplicated_keys} is duplicated"})


def check_value_exists(iterable, key, error_msg="", raise_error=True):
    """
    checks if key not found in iterable of dicts

    optional raise error with custom message or bool
    """
    found = any([element.get(key) for element in iterable])
    if not found and raise_error:
        raise exceptions.ParseError({"error": (f"{key} not exist in given Iterable" if not error_msg else error_msg)})
    return found


class UnlimitedSetPagination(PageNumberPagination):
    page_size = 9999
    page_size_query_param = "page_size"
    max_page_size = 9999


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randomString}".format(slug=slug, randomString=random_string_generator(size=4))

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    # if instance.slug.isnumeric():
    #     raise serializers.ValidationError({"error": "Slug can't be integers only"})
    if instance.slug.isnumeric():
        num_slug = instance.slug
        new_slug = "{slug}-{randomString}".format(slug=num_slug, randomString=random_string_generator(size=4))
        instance.slug = new_slug


def random_path(filename, path):
    time_path = time.strftime("%y/%m/%d")
    ext = filename.split(".")[-1]
    return "{0}/{1}/{2}.{3}".format(path, time_path, random_string_generator(25), ext)


"""
    for dynamic change read only fields for fields control
    at view class add read_only list
    def get_serializer_context(self):
    context = super().get_serializer_context()
    read_only = getattr(self, "read_only", [])
    context["read_only"] = read_only
    return context
    --
    at Serializer class
    def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # dynamic change read_only fields from view
    read_only = self.context.get("read_only", [])
    self.Meta.read_only_fields = (
        read_only
        if not hasattr(self.Meta, "read_only_fields")
        else self.Meta.read_only_fields + read_only
    )
"""


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=1)

    def inactive(self):
        return self.filter(status=0)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()


STATE_CHOICES = (
    ("active", "active"),
    ("pending", "pending"),
    ("deleted", "deleted"),
    ("rejected", "rejected"),
)


class BaseModel(models.Model):
    id = HashidAutoField(primary_key=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
        editable=False,
    )
    created = models.DateTimeField(_("created"), editable=False, auto_now_add=True, blank=True)
    modified = models.DateTimeField(_("modified"), editable=False, auto_now=True, blank=True)

    INACTIVE_STATUS = 0
    ACTIVE_STATUS = 1

    STATUS_CHOICES = (
        (INACTIVE_STATUS, _("Inactive")),
        (ACTIVE_STATUS, _("Active")),
    )
    status = models.IntegerField(_("status"), choices=STATUS_CHOICES, default=ACTIVE_STATUS)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="pending")

    objects = models.Manager()
    custom = ActiveManager()

    class Meta:
        abstract = True

    def state_update(self, state=None):
        if state:
            self.state = state
            self.save()


# class CustomFlexFieldsModelSerializer(CountryFieldMixin, FlexFieldsModelSerializer):
class CustomFlexFieldsModelSerializer(FlexFieldsModelSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # dynamic change read_only fields from view
        read_only = self.context.get("read_only", ())
        self.Meta.read_only_fields = (
            read_only if not hasattr(self.Meta, "read_only_fields") else tuple(itertools.chain(self.Meta.read_only_fields, read_only))
        )

    def save(self, **kwargs):
        try:
            valid = self.context.get("request", [])
            if valid and not isinstance(valid.user, AnonymousUser):
                # TODO use is_authenticated from is better https://docs.djangoproject.com/en/4.2/ref/contrib/auth/ # noqa
                # kwargs.update(created_by=self.context["request"].user)
                pass
        except Exception as e:
            print(e)
        return super().save(**kwargs)


def compress_image(image, quality=50):
    try:
        im = Image.open(image)
    except Exception as e:
        print(e)
        raise exceptions.UnsupportedMediaType(media_type=image.name.split(".")[-1])
    if im.mode != "RGB":
        im = im.convert("RGB")
    im_io = BytesIO()
    ext = image.name.split(".")[-1]
    try:
        im.save(im_io, ext, quality=quality, optimize=True)
    except Exception as e:
        print(e)
        im.save(im_io, "jpeg", quality=quality, optimize=True)
    new_image = File(im_io, name=image.name)
    return new_image
