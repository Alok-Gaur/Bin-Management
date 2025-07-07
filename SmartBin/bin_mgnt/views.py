from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Bin, BinRequest, CleanupRequest, Feedback
from .serializers import (
    BinSerializer, 
    BinRequestSerializer, 
    CleanupRequestSerializer, 
    FeedbackSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()

# Bin Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def bin_list(request):
    bins = Bin.objects.all()
    serializer = BinSerializer(bins, many=True)
    return Response(serializer.data)

# Bin Request Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def bin_request_list(request):
    if request.method == 'GET':
        requests = BinRequest.objects.filter(user=request.user)
        serializer = BinRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BinRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def bin_request_detail(request, pk):
    try:
        bin_request = BinRequest.objects.get(pk=pk, user=request.user)
    except BinRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BinRequestSerializer(bin_request)
        return Response(serializer.data)

# Cleanup Request Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def cleanup_request_list(request):
    if request.method == 'GET':
        requests = CleanupRequest.objects.filter(user=request.user)
        serializer = CleanupRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CleanupRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def cleanup_request_detail(request, pk):
    try:
        cleanup_request = CleanupRequest.objects.get(pk=pk, user=request.user)
    except CleanupRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CleanupRequestSerializer(cleanup_request)
        return Response(serializer.data)

# Feedback Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def feedback_list(request):
    if request.method == 'GET':
        feedbacks = Feedback.objects.filter(user=request.user)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def feedback_detail(request, pk):
    try:
        feedback = Feedback.objects.get(pk=pk, user=request.user)
    except Feedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data)