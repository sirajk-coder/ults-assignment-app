from django.urls import path
from .views import FriendshipRequestView, FriendshipAcceptRejectView, FriendshipListView, PendingFriendshipRequestListView

urlpatterns = [
    path('send-request/', FriendshipRequestView.as_view(), name='send-friend-request'),
    path('accept-reject-request/<int:pk>/', FriendshipAcceptRejectView.as_view(), name='accept-reject-friend-request'),
    path('list-friends/', FriendshipListView.as_view(), name='list-friends'),
    path('pending-requests/', PendingFriendshipRequestListView.as_view(), name='pending-friend-requests'),
]
