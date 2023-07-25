
# Create your tasks here
from celery import shared_task
from project.models import Crawling


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Crawling.objects.count()


@shared_task
def rename_widget(crawling_id, content):
    c = Crawling.objects.get(id=crawling_id)
    c.content = content
    c.save()