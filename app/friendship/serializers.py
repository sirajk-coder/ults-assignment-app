from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import FriendshipRequest, Friendship

class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ('to_user',)

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'
