from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    UserLoginAPIView,
    UserRegistrationAPIView,
    UserLogoutAPIView,
    UserChangePasswordAPIView,
    UserProfileAPIView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='customuser')

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('change-password/', UserChangePasswordAPIView.as_view(), name='change-password'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
