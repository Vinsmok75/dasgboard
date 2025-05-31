# models.py
from django.db import models

# Create your models here.

PROPERTY_TYPES = [
    ('apartment', 'Apartment'),('villa', 'Villa'),('house', 'House'),('land', 'Land'),
]

MOROCCAN_CITIES = [
    ('casablanca', 'Casablanca'),
    ('rabat', 'Rabat'),
    ('marrakech', 'Marrakech'),
    ('fes', 'Fes'),
    ('tangier', 'Tangier'),
    ('agadir', 'Agadir'),
    ('meknes', 'Meknes'),
    ('oujda', 'Oujda'),
    ('kenitra', 'Kenitra'),
    ('tetouan', 'Tetouan'),
    ('safi', 'Safi'),
    ('mohammedia', 'Mohammedia'),
    ('el_jadida', 'El Jadida'),
    ('nador', 'Nador'),
    ('beni_mellal', 'Beni Mellal'),
    ('taza', 'Taza'),
    ('settat', 'Settat'),
]

class Property(models.Model):
    title = models.CharField(max_length=200, help_text='The title of the property')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=0)
    square_meters = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200, choices=MOROCCAN_CITIES)
    property_type = models.CharField(max_length=200, choices=PROPERTY_TYPES)
    views_count = models.PositiveIntegerField(default=0, help_text='Number of times this property has been viewed')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views_count += 1
        self.save()

    class Meta:
        verbose_name_plural = "Properties"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='properties/')
    is_main = models.BooleanField(default=False, help_text='Set this as the main property image')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"

    class Meta:
        ordering = ['-is_main', '-created_at']

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()