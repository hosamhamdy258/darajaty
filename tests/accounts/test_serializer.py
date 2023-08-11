# from rest_framework.exceptions import ValidationError
# from django.test import TestCase
# from accounts.models import User
# from accounts.serializer.user import (
#     CustomUserCreateSerializer,
#     CustomTokenCreateSerializer,
#     CustomUserMeSerializer,
#     CustomUserSerializer,
# )


# class SerializerTestCase(TestCase):
#     def setUp(self):
#         self.valid_data = {
#             "name": "Test User",
#             "password": "StrongPassword123",
#             "email": "test@example.com",
#             "phone": "01234567890",
#         }

#     def test_custom_user_create_serializer(self):
#         serializer = CustomUserCreateSerializer(data=self.valid_data)
#         self.assertTrue(serializer.is_valid())
#         user = serializer.save()
#         self.assertIsInstance(user, User)

#     def test_custom_user_create_serializer_invalid_password(self):
#         invalid_data = self.valid_data.copy()
#         invalid_data["password"] = "weak"
#         serializer = CustomUserCreateSerializer(data=invalid_data)
#         with self.assertRaises(ValidationError):
#             serializer.is_valid(raise_exception=True)

#     def test_custom_token_create_serializer(self):
#         User.objects.create_user(**self.valid_data)
#         valid_token_data = {
#             "password": self.valid_data["password"],
#             "email": self.valid_data["email"],
#         }
#         serializer = CustomTokenCreateSerializer(
#             data=valid_token_data, context={"request": None}
#         )
#         self.assertTrue(serializer.is_valid())

#     def test_custom_token_create_serializer_invalid_credentials(self):
#         invalid_token_data = {
#             "password": "invalid_password",
#             "email": self.valid_data["email"],
#         }
#         serializer = CustomTokenCreateSerializer(
#             data=invalid_token_data, context={"request": None}
#         )
#         with self.assertRaises(ValidationError):
#             serializer.is_valid(raise_exception=True)

#     def test_to_representation_CustomUserMeSerializer(self):
#         user = User.objects.create_user(**self.valid_data)
#         serializer = CustomUserMeSerializer(user).data
#         serializer2 = CustomUserSerializer(user).data
#         self.assertDictEqual(serializer["user"], serializer2)
