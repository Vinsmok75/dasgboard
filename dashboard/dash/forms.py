from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'bedrooms', 'bathrooms',
            'square_meters', 'location', 'property_type',
            'is_published'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'bedrooms': forms.NumberInput(attrs={'min': '0'}),
            'bathrooms': forms.NumberInput(attrs={'min': '0'}),
            'square_meters': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def clean_features(self):
        features = self.cleaned_data.get('features')
        if isinstance(features, str):
            # Convert comma-separated string to list
            features = [f.strip() for f in features.split(',') if f.strip()]
        return features

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_main'] 