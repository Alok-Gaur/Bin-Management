from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
# from .models import my_model


# Create your views here.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def get_material_category(request):
    material_category = MaterialCategory.objects.all()
    if material_category:
        serializer = MaterialCategorySerializer(material_category, many=True)
        return Response(serializer, status=status.HTTP_200_OK)
    return Response({"detail: No Data Found!"}, status= status.HTTP_204_NO_CONTENT)

@api_view(["POST", "PUT"])
@authentication_classes([TokenAuthentication])
def update_material_category(request):
    serializer = MaterialCategorySerializer(data=request.data, partial=True)
    if serializer.is_valid():
        instance = serializer.save()
        response_data = MaterialCategorySerializer(instance).data
        return Response(response_data, status=status.HTTP_200_OK)
    return Response({"detail: Invalid Entry"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def delete_material_category(request, pk):
    try:    
        material_category = MaterialCategory.objects.get(pk=pk)
        material_category.delete()
        return Response({"detail: Deletion Successfull"}, status=status.HTTP_200_OK)
    except MaterialCategory.DoesNotExist:
        return Response({"detail: Material Doesn't Found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def delete_all_material_category(request):
    try:
        material_category = MaterialCategory.objects.all()
        material_category.delete()
        return Response({"detail: Deleteion Successfull"}, status=status.HTTP_200_OK)
    except MaterialCategory.DoesNotExist:
        return Response({"detail: Empty Table"}, status=status.HTTP_204_NO_CONTENT)
        

@api_view(['GET'])
def get_requested_material(request):
    pass

