from django import forms


class UserFollowsForm(forms.Form):
    username = forms.CharField(max_length=100)
    username = forms.CharField(
        max_length=63,
        widget=forms.TextInput(attrs={
            'class': 'px-6 py-2 w-full rounded-md flex-1 outline-none bg-white',
            'placeholder': 'Entrer le nom dutilisateur à chercher'
        })
    )