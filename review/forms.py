from django import forms
from . import models

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body'] 
    
    rating = forms.MultipleChoiceField(
        max_length=63,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300  transition duration-150 ease-in-out'        })
    )

    headline = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300  transition duration-150 ease-in-out',
            'placeholder':'Ajouter un titre'
        })
    )
    body = forms.CharField(
        max_length=63,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300  transition duration-150 ease-in-out',
            'placeholder':'Ajouter un commentaire'
        })
    )