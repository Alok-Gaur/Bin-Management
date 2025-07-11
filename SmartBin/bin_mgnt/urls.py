from django.urls import path
from . import views

# url = "bin/"

urlpatterns = [
    # path('bin-requests/', views.bin_request_list, name='bin-request-list'),
    # path('bin-requests/<int:pk>/', views.bin_request_detail, name='bin-request-detail'),
    # # here should be bin feedbacks
    # path('bin-requests/<int:bin_request_id>/feedbacks/', views.feedback_list, name='feedback-list'),
    # path('bin-requests/<int:bin_request_id>/feedbacks/<int:pk>/', views.feedback_detail, name='feedback-detail'),
    path('status/bin-requests', views.bin_request_status, name='bin-request-status'),
    path('status/clean-requests', views.cleanup_request_status, name='clean-request-status'),
    path('bin-request/', views.bin_request, name="bin-request"),
    path('<int:pk>/clean-request/', views.cleanup_request, name='clean-request')
    
]
