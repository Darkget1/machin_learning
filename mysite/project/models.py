

# Create your models here.
from common.models import User
from django.db import models
from django.utils import dateformat,timezone
import datetime

class Project(models.Model):
    default = 1
    author = models.ForeignKey(User,on_delete=models.SET_DEFAULT,default=default, related_name='author_project')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_project')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    crawling_status = models.IntegerField(default=0)
    target_product = models.CharField(max_length=100,unique=True)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class Project_setting(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    date_1st = models.DateField(default=timezone.now, blank=True)
    date_2nd = models.DateField(default=timezone.now, blank=True)
    brand_add = models.TextField(null=True, blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(default=timezone.now,blank=True)
    mall_name = models.CharField(max_length=10,null=True,blank=True)

class ProjectUrl(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    mall_name = models.CharField(max_length=10)
    url_title = models.CharField(max_length=100,null=True, blank=True)
    url= models.TextField(null=True, blank=True)






