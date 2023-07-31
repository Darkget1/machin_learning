from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from api.serializers import LetterSerializer
from news.models import Letter
from rest_framework.response import Response


# Create your views here.


class LetterViewSet(viewsets.ViewSet):
    def _list(self, request):
        queryset = Letter.objects.all()
        serializer = LetterSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, sid1):
        queryset = Letter.objects.filter(category=sid1)
    #    news = get_object_or_404(queryset, category=sid1)
        serializer = LetterSerializer(queryset, many=True)
        return Response(serializer.data)



        


