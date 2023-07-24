from django.contrib import admin
from news.models import Letter
# Register your models here.

class LetterAdmin(admin.ModelAdmin):
    list_display = ['title','letter_link', 'published_date','preview','writer']
    list_display_links =['title']

admin.site.register(Letter, LetterAdmin)