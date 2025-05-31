from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from dash.models import Property, Contact, PropertyImage
from .serializers import PropertySerializer, ContactSerializer, PropertyImageSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q

class PropertyListAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        print("API endpoint called!")
        
        # Start with published properties only
        queryset = Property.objects.filter(is_published=True)
        print(f"Total published properties: {queryset.count()}")
        
        # Filter by property type
        property_type = self.request.query_params.get('property_type', None)
        if property_type and property_type != 'all':
            queryset = queryset.filter(property_type=property_type)
            print(f"After property_type filter ({property_type}): {queryset.count()}")
        
        # Filter by location (case-insensitive partial match)
        location = self.request.query_params.get('location', None)
        if location and location != 'all':
            queryset = queryset.filter(
                Q(location__icontains=location) | 
                Q(location__iexact=location)
            )
            print(f"After location filter ({location}): {queryset.count()}")
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
                print(f"After min_price filter ({min_price}): {queryset.count()}")
            except ValueError:
                print(f"Invalid min_price value: {min_price}")
        
        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
                print(f"After max_price filter ({max_price}): {queryset.count()}")
            except ValueError:
                print(f"Invalid max_price value: {max_price}")
        
        # Filter by bedrooms
        bedrooms = self.request.query_params.get('bedrooms', None)
        if bedrooms:
            try:
                bedrooms = int(bedrooms)
                queryset = queryset.filter(bedrooms__gte=bedrooms)
                print(f"After bedrooms filter ({bedrooms}+): {queryset.count()}")
            except ValueError:
                print(f"Invalid bedrooms value: {bedrooms}")
        
        # Filter by bathrooms
        bathrooms = self.request.query_params.get('bathrooms', None)
        if bathrooms:
            try:
                bathrooms = int(bathrooms)
                queryset = queryset.filter(bathrooms__gte=bathrooms)
                print(f"After bathrooms filter ({bathrooms}+): {queryset.count()}")
            except ValueError:
                print(f"Invalid bathrooms value: {bathrooms}")
        
        # Order by creation date (newest first)
        queryset = queryset.order_by('-created_at')
        
        print(f"Final queryset count: {queryset.count()}")
        return queryset

    def list(self, request, *args, **kwargs):
        """Override list method to add debugging"""
        print(f"Request query params: {dict(request.query_params)}")
        response = super().list(request, *args, **kwargs)
        print(f"Response data count: {len(response.data) if isinstance(response.data, list) else 'Not a list'}")
        return response

class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.filter(is_published=True)
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the model has increment_views method
        if hasattr(instance, 'increment_views'):
            instance.increment_views()
        else:
            # Fallback: manually increment views_count
            instance.views_count += 1
            instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ContactCreateAPIView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print(f"Contact form submission: {request.data}")
        response = super().create(request, *args, **kwargs)
        print(f"Contact created successfully: {response.data}")
        return response

class PropertyImageAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def post(self, request, property_id):
        property_obj = get_object_or_404(Property, id=property_id)
        serializer = PropertyImageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(property=property_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, property_id, image_id):
        image = get_object_or_404(PropertyImage, id=image_id, property_id=property_id)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
