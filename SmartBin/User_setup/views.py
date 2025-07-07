from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from User_setup.serializers import *
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.

#Login User
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            "user_id": user.id,
            'user_name': user.username,
            'email': user.email,
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Register New User
@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    serializer = UserSignupSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        user = serializer.save()
        print(user)
        token = Token.objects.create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'user_name': user.username,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#View User Profile
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_user_profile(request):
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    except:
        return Response({"error": "profile not found"}, status=status.HTTP_404_NOT_FOUND)

#Create and Update User Profile
@api_view(['POST', 'PUT'])
@authentication_classes([TokenAuthentication])
def update_profile(request):
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    except:
        serializer = UserProfileSerializer(data=request.data)
    
    if serializer.is_valid():
        profile = serializer.save(user = request.user)
        return Response(UserProfileSerializer(profile).data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Delete User Profile
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
def delete_profile(request, user_id):
    if hasattr(request.user, 'profile'):
        request.user.profile.delete()
    else:
        return Response({"detail":"No Profile Found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"detail":"Deletion Successfull"}, status=status.HTTP_200_OK)



#Get all Users
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
# @permission_classes([AllowAny])
def get_user(request):
    users = User.objects.all()
    print(users)
    serializr = UserSerializer(users, many=True)
    print(serializr.data)
    return Response(serializr.data)