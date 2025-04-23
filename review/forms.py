from django import forms
from . import models

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body'] 
    
    RATING_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'flex gap-24 py-2 font-bold'
        })
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