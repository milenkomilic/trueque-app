from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, ItemForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'accounts/index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def password_reset_view(request):
    return render(request, 'accounts/password_reset.html')


def user_profile_view(request):
    return render(request, 'accounts/user_profile.html')

@login_required
def upload_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user  # Asumiendo que el modelo Item tiene un campo 'user'
            item.save()
            # Redirige a donde quieras después de subir el producto, por ejemplo a la página de inicio
            return redirect('index')
    else:
        form = ItemForm()

    return render(request, 'uploads/upload_offer.html', {'form': form})