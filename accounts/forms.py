from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-600 focus:outline-none text-sm font-medium'
    }))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-600 focus:outline-none text-sm font-medium'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-600 focus:outline-none text-sm font-medium'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'e.g., 0541234567',
        'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-600 focus:outline-none text-sm font-medium'
    }))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100 cursor-pointer'
    }))

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'avatar']