# users/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, LoginView, UserSearchView, FriendRequestViewSet

router = DefaultRouter()
router.register(r'friend-requests', FriendRequestViewSet, basename='friend-request')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('', include(router.urls)),
]
