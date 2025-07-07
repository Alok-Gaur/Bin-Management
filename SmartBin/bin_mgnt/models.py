from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Bin(models.Model):
    BIN_TYPES = [
        ('general', 'General Waste'),
        ('recycling', 'Recycling'),
        ('organic', 'Organic Waste'),
    ]
    
    location = models.CharField(max_length=255)
    bin_type = models.CharField(max_length=20, choices=BIN_TYPES)
    capacity = models.PositiveIntegerField(default=100)  # percentage
    last_cleaned = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_bin_type_display()} Bin at {self.location}"

class BinRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bin_requests')
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='requests')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Bin Request #{self.id} - {self.user.username}"

class CleanupRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cleanup_requests')
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name='cleanup_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    completion_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Cleanup Request #{self.id} for {self.bin}"

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    bin_request = models.ForeignKey(BinRequest, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    cleanup_request = models.ForeignKey(CleanupRequest, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback by {self.user.username}"