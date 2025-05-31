from django.contrib import admin

# Register your models here.
from .models import Property, PropertyImage, Contact

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3  # Number of empty forms to display

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'location', 'price', 'is_published', 'created_at')
    list_filter = ('property_type', 'location', 'is_published')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    inlines = [PropertyImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'price', 'property_type', 'location')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'square_meters')
        }),
        ('Status', {
            'fields': ('is_published', 'views_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('property__title',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone', 'message')

