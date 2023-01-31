from rest_framework import serializers
from .models import Item

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['title', 'content']

