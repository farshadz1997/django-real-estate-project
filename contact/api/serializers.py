from rest_framework import serializers
from ..models import Contact


class ContactSerializer(serializers.ModelSerializer):
    def create(self, **validated_data):
        return Contact.objects.create(**validated_data)
    
    class Meta:
        model = Contact
        exclude = ('date',)