from rest_framework import serializers
from .models import Bin, BinRequest, CleanupRequest, Feedback
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ['id', 'location', 'bin_type', 'capacity', 'last_cleaned']

class BinRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    bin = BinSerializer(read_only=True)
    bin_id = serializers.PrimaryKeyRelatedField(queryset=Bin.objects.all(), source='bin', write_only=True)
    
    class Meta:
        model = BinRequest
        fields = ['id', 'user', 'bin', 'bin_id', 'request_date', 'status', 'notes']
        read_only_fields = ['id', 'user', 'request_date', 'status']

class CleanupRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    bin = BinSerializer(read_only=True)
    bin_id = serializers.PrimaryKeyRelatedField(queryset=Bin.objects.all(), source='bin', write_only=True)
    
    class Meta:
        model = CleanupRequest
        fields = ['id', 'user', 'bin', 'bin_id', 'request_date', 'status', 'completion_date', 'notes']
        read_only_fields = ['id', 'user', 'request_date', 'status', 'completion_date']

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    bin_request = serializers.PrimaryKeyRelatedField(queryset=BinRequest.objects.all(), required=False, allow_null=True)
    cleanup_request = serializers.PrimaryKeyRelatedField(queryset=CleanupRequest.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'bin_request', 'cleanup_request', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def validate(self, data):
        if not data.get('bin_request') and not data.get('cleanup_request'):
            raise serializers.ValidationError("Either bin_request or cleanup_request must be provided.")
        if data.get('bin_request') and data.get('cleanup_request'):
            raise serializers.ValidationError("Only one of bin_request or cleanup_request can be provided.")
        return data