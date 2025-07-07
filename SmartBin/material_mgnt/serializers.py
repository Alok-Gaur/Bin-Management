from rest_framework import serializers
from .models import *

class MaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        exclude = ['id']
