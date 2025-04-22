from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

# Premier formulaire (LoginForm)
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-5 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50'
        })
    )
    password = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-5 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50',
            'id': 'password-field' 
        })
    )

# Deuxième formulaire (SignupForm)
class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']
    
    username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-5 pr-4 py-2  rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50'
        })
    )
    
    password1 = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-5 pr-4 py-2 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50'
        })
    )
    
    password2 = forms.CharField(
        max_length=63,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-5 pr-4 py-2 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50'
        })
    )