from common.models import User
from django.db import models

class Posting(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_posting')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_posting')
    def __str__(self):
        return self.subject

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    posting = models.ForeignKey(Posting, null=True, blank=True, on_delete=models.CASCADE)
    # article = models.ForeignKey(Article, null=True,blank=True,on_delete=models.CASCADE)
    #answer = models.ForeignKey(content,null=True,blank=True,on_delete=models.CASCADE)
