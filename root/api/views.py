from django.shortcuts import render

from .serializers import (
    UserRegisterSerializer, 
    UserListSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserPasswordResetSerializer
)

from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import User
from django.contrib.auth import authenticate, login
# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, format = None):
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"Register Successful"}, status = status.HTTP_200_OK)
        else:
            return Response({"Error":"Failed To Register"}, status = status.HTTP_404_NOT_FOUND)
        

    
class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    model = UserListSerializer


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, format = None):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data.get("username")
            password = serializer.data.get("password")
            
            usr = authenticate(username = username, password = password)

            if usr is not None:
                token = get_tokens_for_user(usr)
                return Response(token, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "username or password is not valid"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format = None):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    

class UserPasswordResetView(UpdateAPIView):
    serializer_class =  UserPasswordResetSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset = None):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        #set the new password
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({
            "message":"Password Updated Successful"
        }, status  = status.HTTP_201_CREATED)