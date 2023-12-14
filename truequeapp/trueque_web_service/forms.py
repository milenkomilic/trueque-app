from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Item, Trade
from django.core.exceptions import ValidationError
from datetime import date

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class SetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput())

class CustomUserEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = CustomUser
        fields = ['name', 'lastname', 'lastname_m', 'date_of_birth']

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['responder_item']

class ItemForm(forms.ModelForm):
    image = forms.ImageField(required=True, error_messages={'required': 'Este campo es requerido'})
    class Meta:
        model = Item
        fields = ['title', 'description', 'location', 'price', 'tags', 'active', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={'placeholder': 'Ingrese las etiquetas separadas por comas'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    lastname = forms.CharField(max_length=255, required=True)
    lastname_m = forms.CharField(max_length=255, required=False)
    date_of_birth = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    email = forms.EmailField(required=True)

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise ValidationError("Debes tener al menos 18 años para registrarte.")
        return dob

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

