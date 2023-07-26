from django.db import models
# class naver
# # Create your models here.

class Crawling(models.Model):
    content = models.TextField()



# Create your models here.
class operate_time(models.Model):

    click_time = models.DateTimeField()
    done_time = models.DateTimeField()
    time_gap = models.DurationField()
    click_command = models.CharField(max_length=20)

    def __str__(self):
        return self.click_command

class room(models.Model):
    room_name = models.CharField(max_length=10)