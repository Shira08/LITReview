from django import forms

from . import models

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image',]
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300  transition duration-150 ease-in-out',
            'placeholder':'Ajouter une image'
        })
    )

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'content']
        
    title = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300  transition duration-150 ease-in-out',
            'placeholder':'Ajouter un titre'
        })
    )
    content = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={
             'class': 'w-full pl-5 pr-4 py-2 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white/50',
             'placeholder': 'Ajouter un titre',
             'rows': 4  
    })
)
