

# Create your models here.
from common.models import User
from django.db import models


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_project')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    crawling_status = models.IntegerField(default=0)
    target_product = models.CharField(max_length=100)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.subject
