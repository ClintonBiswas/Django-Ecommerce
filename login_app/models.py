from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email Must Be Set")
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser Must Have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super user must have is_superuser=True')
        return self._create_user(email,password,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=False, unique=True)
    is_staff = models.BooleanField(
        ugettext_lazy('staff status'),
        default = False,
        help_text = ugettext_lazy('Designets whether the user can log in this site')
        )
    is_active = models.BooleanField(
        ugettext_lazy('active'),
        default = True,
        help_text = ugettext_lazy('Designets whether this user should be treated is active. Unselect tis instead of deleted Accounts. ')
        )
    USERNAME_FIELD = 'email'
    object = MyUserManager()

    def __str__(self):
        return self.email
    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=50, blank=True)
    full_name = models.CharField(max_length = 264, blank=True)
    address = models.TextField(blank=True, max_length=300)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(blank=True, max_length = 10)
    phone = models.CharField(blank=True, max_length=20)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s profile'"

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]

        for field_name in fields_names:
            value = getattr(self, field_name)

            if value is None or value=='':
                return False
        return True

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
