import datetime
from django.db import models
# from problems.models import Question
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
    fields = ['_all_']
    username = None
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(max_length=1, null=True,
                              blank=True, choices=GENDER_CHOICES)
    phone_no = PhoneNumberField(null=True, blank=False, unique=True)
    # fields = ['id', 'email', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'is_active',]
    REQUIRED_FIELDS = ['first_name']
    USERNAME_FIELD = 'email'

    def age(self):
        return int((datetime.date.today() - self.birthday).days / 365.25)


class Contact(models.Model):
    name = models.CharField(max_length=155)
    email = models.EmailField()
    subject = models.CharField(max_length=255, default='')
    message = models.TextField()

    def __str__(self):
        return self.name
