from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    lastname = forms.CharField(max_length=255, required=True)
    lastname_m = forms.CharField(max_length=255, required=False)
    date_of_birth = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'lastname', 'lastname_m', 'date_of_birth', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.lastname = self.cleaned_data['lastname']
        user.lastname_m = self.cleaned_data['lastname_m']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user