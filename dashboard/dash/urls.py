# backend/urls.py
from django.urls import path
from .views import PropertyListAPIView, PropertyDetailAPIView, ContactCreateAPIView, PropertyImageView
from . import views

app_name = 'dash'

urlpatterns = [
    # Dashboard URLs
    path('', views.dashboard_home, name='dashboard_home'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('properties/<int:pk>/delete/confirm/', views.property_delete_confirm, name='property_delete_confirm'),
    path('properties/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('properties/<int:pk>/images/', views.property_images, name='property_images'),
    path('properties/<int:pk>/images/<int:image_id>/delete/', views.delete_property_image, name='delete_property_image'),
    path('properties/<int:pk>/increment-views/', views.increment_property_views, name='increment_property_views'),
    
    # API URLs
    path('api/properties/', views.PropertyListAPIView.as_view(), name='api_property_list'),
    path('api/properties/<int:pk>/', views.PropertyDetailAPIView.as_view(), name='api_property_detail'),
    path('api/contacts/', views.ContactCreateAPIView.as_view(), name='api_contact_create'),
    path('api/properties/<int:property_id>/images/', views.PropertyImageView.as_view(), name='api_property_images'),
    path('api/properties/<int:property_id>/images/<int:image_id>/', views.PropertyImageView.as_view(), name='api_property_image_detail'),
]