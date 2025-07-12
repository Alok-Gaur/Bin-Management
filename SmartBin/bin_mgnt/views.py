from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Bin, BinRequest, CleanupRequest, Feedback
from .serializers import *
from django.contrib.auth import get_user_model

User = get_user_model()


"""
API Description of the View

1. bin_list : Get all the bin data or all the bins present in the database, either requested or completed
2. bin_request_list: Get all the bins requested by the user and their status or Request a new bin
3. 
"""




# Get all Bin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_all_bin(request):
    """Get all the bins present in the database (established and requested)"""
    bins = Bin.objects.all()
    serializer = BinSerializer(bins, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_requested_bins(request):
    '''Get all the bin request raised by the user'''
    user = request.user
    bin_requests = user.bin_requests.all()
    if bin_requests:
        serializer = BinRequestSerializer(bin_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'response': "No request raised!"})



# Request a Bin or View all requested Bins
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def bin_request(request):
    '''Raise a request for the bin'''
    serializer = BinRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# This is just a prototype. Don't concer yourself to it
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def bin_request_detail(request, pk):
    '''Get the details of the specific bin'''
    try:
        bin_request = BinRequest.objects.get(pk=pk, user=request.user)
    except BinRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BinRequestSerializer(bin_request)
    return Response(serializer.data)



@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_requested_cleanups(request):
    '''get all the cleanup requests raised'''
    user = request.user
    clean_request = user.cleanup_requests.all()
    if clean_request:
        serializer = CleanupRequestViewSerializer(clean_request, manay=True)
        return Response(serializer.data, status.HTTP_200_OK)
    return Response({'response': "No Request Found!"}, status.HTTP_404_NOT_FOUND)



# Raise Cleanup Request
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def cleanup_request(request, pk):
    """raise a cleanup request of a specific bin"""  
    request.data.update({
        "bin": pk
    })
    serializer = CleanupRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Don't concern yourself with this function
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def cleanup_request_detail(request, pk):
    """ Get the details about the request/ request form"""
    try:
        cleanup_request = CleanupRequest.objects.get(pk=pk, user=request.user)
    except CleanupRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CleanupRequestSerializer(cleanup_request)
        return Response(serializer.data)



@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_feedbacks(request, id):
    feedback = Feedback.objects.filter(user=request.user).get(pk=id)
    serializer = FeedbackViewSerializer(feedback)
    return Response(serializer.data)



# Feedback Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def feedback(request):    
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
    
    
    
# Here comes the main part

