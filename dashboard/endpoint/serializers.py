from rest_framework import serializers
from dash.models import Property, Contact, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_main']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True, context={'request': None})
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 
            'title', 
            'price', 
            'bedrooms', 
            'bathrooms', 
            'square_meters',
            'location', 
            'images', 
            'main_image', 
            'property_type', 
            'description', 
            'is_published', 
            'created_at', 
            'views_count'
        ]

    def get_main_image(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image and main_image.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_image.image.url)
            return main_image.image.url
        return None
    
    def to_representation(self, instance):
        """Override to pass request context to nested serializers"""
        representation = super().to_representation(instance)
        request = self.context.get('request')
        
        # Update images with proper context
        if request:
            images_data = []
            for image in instance.images.all():
                image_serializer = PropertyImageSerializer(image, context={'request': request})
                images_data.append(image_serializer.data)
            representation['images'] = images_data
        
        return representation

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
    
    def validate_email(self, value):
        """Validate email format"""
        if '@' not in value:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value
