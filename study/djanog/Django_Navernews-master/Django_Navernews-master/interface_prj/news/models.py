from django.db import models
from django.utils import timezone

# Create your models here.


#class Category(models.Model):

class Letter(models.Model):
    # 큰 주제
    category = models.CharField(max_length=10, default="", null=True)
    # 작은 주제
    topic = models.CharField(max_length=10, default="", null=True)
    # 기사제목
    title = models.CharField(max_length=100,default="", primary_key=True)
    # 기사링크
    letter_link = models.URLField(max_length=100)
    # 날짜
    published_date = models.CharField(max_length=20, default="", null=True)
    # 조회 시간
    created_date = models.DateTimeField(default=timezone.now)
    # 미리보기
    preview = models.TextField()
    # 신문사
    writer = models.CharField(max_length=20,default="", null=True)

    def __str__(self):
        return self.title



