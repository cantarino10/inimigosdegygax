from rest_framework import serializers
from main import models

class FeatsSerializer(serializers.ModelSerializer):
  class Meta:  
    model = models.Feats
    fields = '__all__'