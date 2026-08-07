from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin,BaseUserManager

# class CustomUserModel(AbstractUser):
#     id_code=models.CharField(blank=True, max_length=12)
#     phone=models.CharField(blank=True, max_length=12)


class CustomeUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        if extra_fields.get("is_verified") is not True:
            raise ValueError(("Superuser must have is_verified=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    objects = CustomeUserManager()

    def __str__(self):
        return self.email
import uuid   
def default_phone():
    # 09 + 9 رقم = 11 رقم
    return "09" + str(uuid.uuid4().int)[:9]


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    id_card = models.UUIDField(default=uuid.uuid4,unique=True)

    phone = models.CharField(max_length=11,unique=True,default=default_phone)

    image = models.ImageField(upload_to='accounts/', blank=True)
    def __str__(self):
        return self.user.email