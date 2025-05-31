# backend/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Property, Contact, PropertyImage, PROPERTY_TYPES, MOROCCAN_CITIES
from .serializers import PropertySerializer, PropertyDetailSerializer, ContactSerializer, PropertyImageSerializer
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import PropertyForm, PropertyImageForm

# API Views
class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer

class ContactCreateAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class PropertyImageView(generics.GenericAPIView):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer

    def post(self, request, property_id):
        property = get_object_or_404(Property, id=property_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(property=property)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, property_id, image_id):
        image = get_object_or_404(PropertyImage, id=image_id, property_id=property_id)
        image.delete()
        return Response(status=204)

# Dashboard Views
def dashboard_home(request):
    total_properties = Property.objects.count()
    recent_properties = Property.objects.order_by('-created_at')[:5]
    
    context = {
        'total_properties': total_properties,
        'recent_properties': recent_properties,
        'active_page': 'dashboard'
    }
    return render(request, 'dash/dashboard_home.html', context)

def property_list(request):
    properties = Property.objects.prefetch_related('images').all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    property_type = request.GET.get('type', '')
    location = request.GET.get('location', '')
    
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if property_type:
        properties = properties.filter(property_type=property_type)
        
    if location:
        properties = properties.filter(location=location)
    
    # Pagination
    paginator = Paginator(properties, 9)  # Show 9 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'properties': page_obj,
        'search_query': search_query,
        'property_type': property_type,
        'location': location,
        'property_types': PROPERTY_TYPES,
        'cities': MOROCCAN_CITIES,
        'active_page': 'properties'
    }
    return render(request, 'dash/property_list.html', context)

def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save()
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                PropertyImage.objects.create(
                    property=property,
                    image=image,
                    is_main=(i == 0)  # First image is main by default
                )
            
            messages.success(request, 'Property created successfully!')
            return redirect('dash:property_list')
    else:
        form = PropertyForm()
    
    return render(request, 'dash/property_form.html', {
        'form': form,
        'active_page': 'create'
    })

def property_edit(request, pk):
    property = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('dash:property_list')
    else:
        form = PropertyForm(instance=property)
    
    return render(request, 'dash/property_form.html', {
        'form': form,
        'property': property,
        'active_page': 'properties'
    })

def property_delete_confirm(request, pk):
    property = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        # Delete the property and its associated images
        property.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('dash:property_list')
        
    return render(request, 'dash/property_delete_confirm.html', {
        'property': property,
        'active_page': 'properties'
    })

def property_delete(request, pk):
    if request.method == 'POST':
        property = get_object_or_404(Property, pk=pk)
        property.delete()
        messages.success(request, 'Property deleted successfully!')
    return redirect('dash:property_list')

def property_images(request, pk):
    property = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PropertyImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.property = property
            
            # If this is marked as main image, unmark others
            if image.is_main:
                property.images.filter(is_main=True).update(is_main=False)
            
            image.save()
            messages.success(request, 'Image added successfully!')
            return redirect('dash:property_images', pk=pk)
    else:
        form = PropertyImageForm()
    
    return render(request, 'dash/property_images.html', {
        'property': property,
        'form': form,
        'active_page': 'properties'
    })

def delete_property_image(request, pk, image_id):
    if request.method == 'POST':
        image = get_object_or_404(PropertyImage, id=image_id, property_id=pk)
        image.delete()
        messages.success(request, 'Image deleted successfully!')
        return redirect('dash:property_images', pk=pk)
    return JsonResponse({'status': 'error'}, status=400)

def increment_property_views(request, pk):
    if request.method == 'POST':
        property = get_object_or_404(Property, pk=pk)
        property.increment_views()
        return JsonResponse({'status': 'success', 'views': property.views_count})
    return JsonResponse({'status': 'error'}, status=400)