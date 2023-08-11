from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from hashid_field import HashidAutoField
from django.db.models.constraints import CheckConstraint
from django.db.models import Q


from wallet.models import Wallet


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, phone, password):
        user = self.model(email=self.normalize_email(email), name=name, phone=phone)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        Wallet.objects.create(user=user)
        return user

    def create_superuser(self, email, name, phone, password):
        user = self.create_user(
            email=self.normalize_email(email), name=name, phone=phone, password=password
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)

        return user


regex = r"^01[0125][0-9]{8}$"


class User(AbstractBaseUser):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(phone__regex=regex), name="phone_number")
        ]

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("name", "phone")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date Joined")
    last_update = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin
