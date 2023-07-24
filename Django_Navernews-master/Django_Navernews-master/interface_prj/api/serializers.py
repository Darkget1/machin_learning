from rest_framework import serializers
from news.models import Letter

class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields=('category','topic','writer')