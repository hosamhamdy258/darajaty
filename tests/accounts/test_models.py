# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from accounts.models import User
# from wallet.models import Wallet


# class UserModelTestCase(TestCase):
#     def setUp(self):
#         self.user_data = {
#             "email": "test@example.com",
#             "name": "Test User",
#             "phone": "01234567891",
#             "password": "testpassword",
#         }

#     def test_user_creation(self):
#         user = User.objects.create_user(**self.user_data)
#         self.assertEqual(user.email, self.user_data["email"])
#         self.assertEqual(user.name, self.user_data["name"])
#         self.assertEqual(user.phone, self.user_data["phone"])
#         self.assertTrue(user.check_password(self.user_data["password"]))
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_admin)
#         self.assertEqual(user.is_staff, user.is_admin)

#     def test_superuser_creation(self):
#         user = User.objects.create_superuser(**self.user_data)
#         self.assertEqual(user.email, self.user_data["email"])
#         self.assertEqual(user.name, self.user_data["name"])
#         self.assertEqual(user.phone, self.user_data["phone"])
#         self.assertTrue(user.check_password(self.user_data["password"]))
#         self.assertTrue(user.is_active)
#         self.assertTrue(user.is_admin)
#         self.assertEqual(user.is_staff, user.is_admin)

#     def test_phone_regex_validation(self):
#         self.user_data["phone"] = "invalid-phone"

#         with self.assertRaises(ValidationError):
#             User.objects.create_user(**self.user_data)

#     def test_email_validator(self):
#         self.user_data["email"] = "invalid-email"

#         with self.assertRaises(ValidationError):
#             User.objects.create_user(**self.user_data)

#     def test_wallet_creation(self):
#         user = User.objects.create_user(**self.user_data)
#         wallet = Wallet.objects.get(user=user)
#         self.assertEqual(wallet.current_balance, 0)

#     def test_user_permissions(self):
#         user = User.objects.create_user(**self.user_data)
#         self.assertTrue(user.has_perm("some_permission"))
#         self.assertTrue(user.has_module_perms("some_app_label"))

#     def test_str_representation(self):
#         user = User.objects.create_user(**self.user_data)
#         self.assertEqual(str(user), self.user_data["email"])

#     def test_email_uniqueness(self):
#         User.objects.create_user(**self.user_data)
#         with self.assertRaises(ValidationError):
#             User.objects.create_user(**self.user_data)

#     def test_inactive_user(self):
#         user = User.objects.create_user(**self.user_data)
#         user.is_active = False
#         user.save()
#         self.assertFalse(user.is_active)

#     def test_username_field(self):
#         # Test username field should be 'email'
#         user = User.objects.create_user(**self.user_data)
#         self.assertEqual(user.USERNAME_FIELD, "email")

#     def test_date_fields(self):
#         # Test auto_now and auto_now_add fields
#         user = User.objects.create_user(**self.user_data)
#         self.assertIsNotNone(user.date_joined)
#         old_last_update = user.last_update
#         user.name = "Updated Name"
#         user.save()
#         self.assertNotEqual(user.last_update, old_last_update)

#     def test_manager_create_user_without_name(self):
#         self.user_data.pop("name")
#         with self.assertRaises(TypeError):
#             User.objects.create_user(**self.user_data)

#     def test_manager_create_user_without_email(self):
#         self.user_data.pop("email")
#         with self.assertRaises(TypeError):
#             User.objects.create_user(**self.user_data)

#     def test_manager_create_user_without_phone(self):
#         self.user_data.pop("phone")
#         with self.assertRaises(TypeError):
#             User.objects.create_user(**self.user_data)

#     def test_manager_create_user_without_password(self):
#         self.user_data.pop("password")
#         with self.assertRaises(TypeError):
#             User.objects.create_user(**self.user_data)
