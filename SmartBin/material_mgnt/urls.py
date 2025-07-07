from django.urls import path
from . import views
urlpatterns = [
    path('request/', views.get_requested_material)
]