from django import forms
from .models import ItemListing

class AdSubmissionForm(forms.ModelForm):
    class Meta:
        model = ItemListing
        fields = [
            'title', 'category', 'location', 'price', 
            'is_negotiable', 'condition', 'description', 
            'phone_number', 'whatsapp_number'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg', 'placeholder': 'e.g., Slightly used Samsung A52'}),
            'category': forms.Select(attrs={'class': 'w-full p-3 border rounded-lg'}),
            'location': forms.Select(attrs={'class': 'w-full p-3 border rounded-lg'}),
            'price': forms.NumberInput(attrs={'class': 'w-full p-3 border rounded-lg', 'placeholder': 'GHS'}),
            'condition': forms.Select(attrs={'class': 'w-full p-3 border rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-lg', 'rows': 4, 'placeholder': 'Describe item condition...'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg', 'placeholder': '024XXXXXXX'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg', 'placeholder': '024XXXXXXX (Optional)'}),
        }