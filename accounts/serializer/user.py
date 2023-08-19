from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.conf import settings
from djoser.serializers import (
    TokenCreateSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from hashid_field import HashidField
from hashid_field.rest import HashidSerializerCharField
from rest_framework import serializers

from accounts.models import User
from core.extensions.utils import CustomFlexFieldsModelSerializer


class CustomUserCreateSerializer(CustomFlexFieldsModelSerializer, UserCreateSerializer):
    # id = HashidSerializerCharField(source_field=HashidField(), read_only=True)

    class Meta:
        model = User
        fields = ("name", "password", "email", "phone")

    def validate(self, attrs):
        password = attrs.get("password")
        try:
            validate_password(password)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        user = super().create(validated_data)
        return user


class CustomUserSerializer(CustomFlexFieldsModelSerializer, UserSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "is_admin", "email", "phone")


class CustomUserMeSerializer(CustomFlexFieldsModelSerializer, UserSerializer):
    id = HashidSerializerCharField(source_field=HashidField(), read_only=True)

    class Meta:
        model = User
        fields = ("id",)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = CustomUserSerializer(instance=instance).data
        return rep


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            attrs["user"] = self.user
            return attrs
        self.fail("invalid_credentials")
