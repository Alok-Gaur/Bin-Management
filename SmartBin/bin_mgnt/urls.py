from django.urls import path
from . import views

urlpatterns = [
    path('bin-requests/', views.bin_request_list, name='bin-request-list'),
    path('bin-requests/<int:pk>/', views.bin_request_detail, name='bin-request-detail'),
    path('bin-requests/<int:bin_request_id>/feedbacks/', views.feedback_list, name='feedback-list'),
    path('bin-requests/<int:bin_request_id>/feedbacks/<int:pk>/', views.feedback_detail, name='feedback-detail'),
]
