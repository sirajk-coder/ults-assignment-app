from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FriendshipRequest, Friendship
from .serializers import FriendshipRequestSerializer, FriendshipSerializer
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class FriendshipRequestView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = FriendshipRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if the user has sent more than 3 requests within the last minute
        recent_requests = FriendshipRequest.objects.filter(
            from_user=request.user,
            created_at__gte=datetime.now() - timedelta(minutes=1)
        )
        if recent_requests.count() >= 3:
            return Response({"detail": "You cannot send more than 3 friend requests within a minute."},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Set the from_user field to the current user before saving
        serializer.validated_data['from_user'] = self.request.user
        instance = serializer.save()

        # Set the friendship field upon creation
        if instance.status == 'accepted':
            friendship = Friendship.objects.create(user1=instance.from_user, user2=instance.to_user)
            instance.friendship = friendship
            instance.save()

class FriendshipAcceptRejectView(generics.UpdateAPIView):
    serializer_class = FriendshipRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.to_user != request.user:
            return Response({"detail": "You are not allowed to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        if 'accept' in request.data:
            instance.status = 'accepted'
            Friendship.objects.create(user1=instance.from_user, user2=instance.to_user)
        elif 'reject' in request.data:
            instance.status = 'rejected'

        instance.save()
        return Response({"detail": "Friendship request updated successfully."})

class FriendshipListView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(user1=self.request.user) | Friendship.objects.filter(user2=self.request.user)

class PendingFriendshipRequestListView(generics.ListAPIView):
    serializer_class = FriendshipRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendshipRequest.objects.filter(to_user=self.request.user, status='pending')
