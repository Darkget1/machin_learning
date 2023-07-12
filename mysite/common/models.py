from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    first_name = models.CharField("성", max_length=20, null=True, blank=True)
    last_name = models.CharField("이름", max_length=20, null=True, blank=True)
    tel = models.CharField("연락처", max_length=20, null=True, blank=True)
    create_date = models.DateTimeField('생성일', null=True, blank=True)
    modify_date = models.DateTimeField(null=True,blank=True)

