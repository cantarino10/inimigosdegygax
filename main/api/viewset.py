from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from main.api import serializers
from main import models

class FeatsViewSet(viewsets.ModelViewSet):
  #permission_classes = (IsAuthenticated,)
  serializer_class = serializers.FeatsSerializer
  queryset = models.Feats.objects.all()