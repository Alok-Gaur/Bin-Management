from rest_framework import serializers
from .models import Bin, BinRequest, CleanupRequest, Feedback
from django.contrib.auth import get_user_model
from django.db.models import Q, F

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ['id', 'location', 'bin_type', 'capacity', 'last_cleaned']



# class BinRequestSerializer(serializers.ModelSerializer):
#     notes = serializers.CharField(required=False, allow_blank=True)
#     location = serializers.CharField(max_length=255, write_only=True)
#     bin_type = serializers.CharField(max_length=20, required=False, write_only=True)
    
#     bin_type = serializers.CharField(source="Bin.bin_type", read_only=True)
    
    
    
#     class Meta:
#         model = BinRequest
#         fields = ['id', 'bin', 'request_date', 'status', 'notes', "bin_type", "location"]
#         read_only_fields = ['id','bin_type', 'request_date', 'status', 'bin']
    
#     def validate(self, data):
#         request = self.context['request']
#         user = request.user
#         location = data.get('location')
#         # check_bin_location = Bin.objects.filter(location=location, installed_date__isnull=True).all()
        
#         request_raised = user.bin_requests.filter(bin__location=location).first()
#         if request_raised:
#             raise serializers.ValidationError(f"Bin request already raised for location: {location}")
#         return data
    
#     def create(self, validated_data):
#         request = self.context['request']
        
#         location = validated_data.get("location")
#         bin_type = validated_data.get("bin_type")
        
#         check_bin = Bin.objects.filter(location=location).filter(request_count__gte=1)
#         if check_bin:
#             check_bin.update(request_count=F('request_count')+1)
#             check_bin = check_bin.first()
#         else:
#             check_bin = Bin.objects.create(location=location, bin_type=bin_type, request_count=1)
        
#         user = request.user
#         bin_request = BinRequest.objects.create(user=user, bin=check_bin, notes=validated_data.get("notes"))
#         return bin_request

class BinRequestSerializer(serializers.ModelSerializer):
    bin_type = serializers.CharField(max_length=20, write_only=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(max_length=255, write_only=True)
    
    class Meta:
        model = BinRequest
        fields=["notes", "location", "bin_type"]
    
    def validate(self, data):
        request = self.context['request']
        user = request.user
        
        location = data.get("location")
        
        request_raised = user.bin_requests.filter(bin__location=location).first()
        if request_raised:
            raise serializers.ValidationError(f"Bin Request Already Raised for Location: {location}")
        return data
    
    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        
        location = validated_data.get("location")
        bin_type = validated_data.get("bin_type")
        
        check_bin = Bin.objects.filter(location=location).filter(request_count__gte=1)
        if check_bin:
            check_bin.update(request_count=F('request_count')+1)
            check_bin = check_bin.first()
        else:
            check_bin = Bin.objects.create(location=location, bin_type=bin_type, request_count=1)
        bin_request = BinRequest.objects.create(user=user, bin=check_bin, notes=validated_data.get("notes"))
        return bin_request



class BinRequestViewSerializer(serializers.ModelSerializer):
    bin_type = serializers.CharField(source='bin.bin_type')
    class Meta:
        model = BinRequest
        fields = ['bin', 'request_date', 'status', 'bin_type', 'location']
    

class CleanupRequestSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # bin = BinSerializer(read_only=True)
    bin_id = serializers.PrimaryKeyRelatedField(queryset=Bin.objects.all(), source='bin', write_only=True)
    
    class Meta:
        model = CleanupRequest
        fields = ['bin_id', 'request_date', 'status', 'completion_date', 'notes']
        read_only_fields = ['request_date', 'status', 'completion_date']

    def create(self, validated_data):
        user = self.context['request']
        bin_id = validated_data.pop("bin_id")
        
        try:
            check_bin = Bin.objects.filter(pk=bin_id)
            if check_bin:
                check_bin.update(clean_request_count=F("clean_request_count")+1)
                bin = check_bin.first()
                validated_data['user'] = user
                validated_data['bin'] = bin
                data = CleanupRequest.objects.create(**validated_data)
                return data
        except Exception as e:
            serializers.ErrorDetail(f"Bin {bin_id} doesn't exists!")
        return ""
            


class CleanupRequestViewSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='bin.location', read_only=True)
    class Meta:
        model = CleanupRequest
        fields = ['bin', 'request_date', 'status', 'completion_date', 'location']



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

class FeedbackSerializer(serializers.ModelSerializer):
    raised = serializers.CharField(max_length=20, write_only=True)
    raised_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Feedback
        fields = ['raised', 'raised_id', 'rating', 'comment']
    
    def create(self, validated_data, **kwargs):
        user = kwargs.get('user')
        raised = validated_data.pop('raised')
        raised_id = validated_data.pop('raised_id')
        validated_data.update({
            f"{raised}_id": raised_id
        })
        data = Feedback.objects.create(user=user, **validated_data)
        return data

class FeedbackViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"