from django.urls import path
from . import views

# url = "bin/"

urlpatterns = [
    path('status/bin-requests', views.get_requested_bins, name='get-requested-bins'),
    path('status/clean-requests', views.get_requested_cleanups, name='get-requested-cleanup'),
    path('bin-request/', views.bin_request, name="bin-request"),
    path('<int:pk>/clean-request/', views.cleanup_request, name='clean-request'),
    path('get-feedback/<int:id>/', views.get_feedbacks, name='get-feedback'),
    path('feedback/', views.feedback, name="feedback")
]
