from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Project_setting,Project

#프로젝트 생성시 프로젝트 셋팅 자동생성
@receiver(post_save, sender=Project)
def creat_project(sender, instance, created, **kwargs):
    if created:
        Project_setting.objects.create(project=instance)