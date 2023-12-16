from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name','last_name')
        extra_kwargs = {'password': {'write_only': True},'email':{'validators': [UniqueValidator(queryset=User.objects.all())
            ]}}

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','first_name','last_name')
