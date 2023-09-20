from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, name, age, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            age=age
        )

        user.is_active = True
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, age, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            name = name,
            age = age,
            password = password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'age']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username