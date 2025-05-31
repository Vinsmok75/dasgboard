from django.urls import path
from . import views

app_name = 'endpoint'

urlpatterns = [
    # Property endpoints
    path('properties/', views.PropertyListAPIView.as_view(), name='property_list'),
    path('properties/<int:pk>/', views.PropertyDetailAPIView.as_view(), name='property_detail'),
    
    # Contact endpoint
    path('contacts/', views.ContactCreateAPIView.as_view(), name='contact_create'),
    
    # Property images endpoints
    path('properties/<int:property_id>/images/', views.PropertyImageAPIView.as_view(), name='property_images'),
    path('properties/<int:property_id>/images/<int:image_id>/', views.PropertyImageAPIView.as_view(), name='property_image_detail'),
] 