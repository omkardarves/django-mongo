# person/serializers.py

from rest_framework import serializers

class MyApiSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
