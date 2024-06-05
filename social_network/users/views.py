from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, generics, permissions
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import ScopedRateThrottle
from django.contrib.auth import get_user_model
from .models import FriendRequest
from .serializers import UserSerializer, SignupSerializer, FriendRequestSerializer

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class UserSearchView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^username']

class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'friend_request'

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

    def get_queryset(self):
        if self.action == 'list':
            return FriendRequest.objects.filter(to_user=self.request.user, is_accepted=False)
        return super().get_queryset()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'is_accepted' in request.data:
            instance.is_accepted = request.data['is_accepted']
            instance.save()
        return super().update(request, *args, **kwargs)
