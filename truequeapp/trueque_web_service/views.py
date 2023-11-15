from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, ItemForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage
from .models import Item

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

@login_required
def user_profile_view(request):
    return render(request, 'accounts/user_profile.html')

@login_required
def upload_item_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.date_posted = timezone.now()  # Asigna manualmente la fecha y hora actuales
            item.save()
            return redirect('index')
    else:
        form = ItemForm()

    return render(request, 'items/upload_offer.html', {'form': form})

@login_required
def view_items(request):
    item_list = Item.objects.all()
    paginator = Paginator(item_list, 10)  # Muestra 10 items por página

    page_number = request.GET.get('page', 1)  # Obtén el número de página, predeterminado a 1
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(1)  # Si la página no existe, muestra la primera página

    return render(request, 'items/view_items.html', {'page_obj': page_obj})