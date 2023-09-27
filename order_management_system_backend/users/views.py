from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, pagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from datetime import datetime
from django.db.models import Q

from .recaptcha_util import verify_recaptcha
from .models import CustomUser
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserChangePasswordSerializer
)

import requests

class UserLoginAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    
    def post(self, request):
        captcha_response = request.data.get('g-recaptcha-response', None)
        
        if not captcha_response:
            return Response({'message': 'Invalid reCAPTCHA'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_valid_captcha = verify_recaptcha(captcha_response)

        if not is_valid_captcha:
            return Response({'message': 'Invalid reCAPTCHA'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(CustomUser, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'message': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({
            'token': token.key,
            'email': serializer.data['email'],
            'username': serializer.data['username'],
            'name': serializer.data['name'],
            'is_superuser': serializer.data['is_superuser'],
            'is_staff': serializer.data['is_staff']
        })

class UserRegistrationAPIView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():

            captcha_response = request.data.get('g-recaptcha-response', None)
            
            if not captcha_response:
                return Response({'message': 'Invalid reCAPTCHA'}, status=status.HTTP_400_BAD_REQUEST)
            
            is_valid_captcha = verify_recaptcha(captcha_response)

            if not is_valid_captcha:
                return Response({'message': 'Invalid reCAPTCHA'}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPagination(pagination.PageNumberPagination):
    page_size = 10  # Number of users per page
    page_size_query_param = 'page_size'

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = CustomUser.objects.all()
            
            age = request.query_params.get('age')
            if age:
                try:
                    age = int(age)
                    if 18 <= age <= 70:
                        queryset = queryset.filter(age=age)
                    else:
                        return Response({'message': 'Age is out of range.'}, status=status.HTTP_400_BAD_REQUEST)
                except ValueError:
                    return Response({'message': 'Not a valid int for age.'}, status=status.HTTP_400_BAD_REQUEST)
            
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                queryset = queryset.filter(date_joined__range=(start_date, end_date))

            keyword = request.query_params.get('keyword')
            if keyword:
                queryset = queryset.filter(Q(username__icontains=keyword) | Q(email__icontains=keyword) | Q(name__icontains=keyword))
            
        else:
            queryset = CustomUser.objects.none()
            return Response(
                {'message': 'You do not have permission to view users.'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if (
            request.user == instance.user or
            request.user.is_staff or
            request.user.is_superuser
        ):
            instance.is_active = False
            instance.save()
            return Response({'message': 'User deactivated successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'message': 'You do not have permission to delete this trade.'},
                status=status.HTTP_403_FORBIDDEN
            )

class UserLogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

class UserChangePasswordAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def post(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(current_password):
                return Response({'error': 'Incorrect current password'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)