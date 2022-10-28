from rest_framework import serializers
from ..models import Profile
from django.contrib.auth.models import User
from django.db.models import Q


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate_password2(self, value):
        password1 = self.initial_data.get("password")
        password2 = value
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return value
    
    def validate_email(self, value):
        email = value
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def validate_username(self, value):
        username = value
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create(**validated_data)
    
    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")