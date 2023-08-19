from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings


class ExtraFeatures:
    """
    Apply this mixin to any view or viewSet to add multiple features
    - control serializer class meta fields by override fields/omit = list or tuple
    - use expand to force expand on serializer class inherited
    from rest_flex_fields import FlexFieldsModelSerializer
    - use read_only = list or tuple to force readonly field on serializer class
    """

    fields = []
    omit = []
    expand = []
    read_only = []

    def get_serializer_context(self):
        context = super().get_serializer_context()
        read_only = self.read_only if isinstance(self.read_only, (list, tuple)) else []
        context["read_only"] = read_only
        return context

    def extra_fields(self):
        def err(key):
            raise ValidationError({"error": f"{key} must be list or tuple"})

        fields = (
            self.fields if isinstance(self.fields, (list, tuple)) else err("fields")
        )
        omit = self.omit if isinstance(self.omit, (list, tuple)) else err("omit")
        expand = (
            self.expand if isinstance(self.expand, (list, tuple)) else err("expand")
        )
        return [fields, omit, expand]


class MultipleFieldLookupMixin:
    lookup_fields = ["pk"]
    """
    Apply this mixin to any view or viewSet to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    don't forget to override field lookup_fields = ["pk" ,'slug'] in the child class
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        fields, omit, expand = self.extra_fields()
        serializer = self.get_serializer(
            data=request.data, fields=fields, omit=omit, expand=expand
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        fields, omit, expand = self.extra_fields()
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, fields=fields, omit=omit, expand=expand
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, fields=fields, omit=omit, expand=expand
        )
        return Response(serializer.data)


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        fields, omit, expand = self.extra_fields()
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, fields=fields, omit=omit, expand=expand
        )
        return Response(serializer.data)


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        fields, omit, expand = self.extra_fields()
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            fields=fields,
            omit=omit,
            expand=expand,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CreateAPIView(
    MultipleFieldLookupMixin, ExtraFeatures, CreateModelMixin, GenericAPIView
):
    """
    Concrete view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListAPIView(
    MultipleFieldLookupMixin, ExtraFeatures, ListModelMixin, GenericAPIView
):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(
    MultipleFieldLookupMixin, ExtraFeatures, RetrieveModelMixin, GenericAPIView
):
    """
    Concrete view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DestroyAPIView(
    MultipleFieldLookupMixin, ExtraFeatures, DestroyModelMixin, GenericAPIView
):
    """
    Concrete view for deleting a model instance.
    """

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateAPIView(
    MultipleFieldLookupMixin, ExtraFeatures, UpdateModelMixin, GenericAPIView
):
    """
    Concrete view for updating a model instance.
    """

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed(method="PUT")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListCreateAPIView(
    MultipleFieldLookupMixin,
    ExtraFeatures,
    ListModelMixin,
    CreateModelMixin,
    GenericAPIView,
):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateAPIView(
    MultipleFieldLookupMixin,
    ExtraFeatures,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericAPIView,
):
    """
    Concrete view for retrieving, updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed(method="PUT")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RetrieveDestroyAPIView(
    MultipleFieldLookupMixin,
    ExtraFeatures,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericAPIView,
):
    """
    Concrete view for retrieving or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(
    MultipleFieldLookupMixin,
    ExtraFeatures,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericAPIView,
):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        raise MethodNotAllowed(method="PUT")
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
