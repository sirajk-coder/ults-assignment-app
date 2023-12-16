from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserSerializer, UserSearchSerializer
from django.contrib.auth.models import User

class UserSignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(password=make_password(serializer.validated_data['password']),username=serializer.validated_data['email'])
        Token.objects.create(user=user)

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['username'] = data.get('email')
        serializer = self.serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'email': user.email})
    

class UserSearchView(ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_term = self.request.query_params.get('key', None)
        if not search_term or search_term.strip() == '':
            return User.objects.none()

        
        if '@' in search_term: # Search by exact email
            queryset = User.objects.filter(Q(email=search_term) | Q(username=search_term))
        else:
            queryset = User.objects.filter(Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term))
        return queryset.exclude(id=self.request.user.id)
