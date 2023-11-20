from gettext import translation
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Item, Trade, CustomUser
from .forms import CustomUserCreationForm, ItemForm
from .forms import TradeForm
from django.contrib import messages




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
    items_list = Item.objects.all()  # Asegúrate de que esto obtiene los items correctos
    paginator = Paginator(items_list, 4)  # Muestra 10 items por página

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, muestra la primera página.
        items = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, muestra la última página de resultados.
        items = paginator.page(paginator.num_pages)

    return render(request, 'items/view_items.html', {'page_obj': items})

@login_required
def initiate_trade(request, item_id):
    item_to_trade = get_object_or_404(Item, id=item_id, active=True)
    user_items = Item.objects.filter(user=request.user, active=True).exclude(id=item_id)
    
    if request.method == 'POST':
        responder_item_id = request.POST.get('responder_item')
        responder_item = get_object_or_404(Item, id=responder_item_id, user=request.user, active=True)

        existing_trade = Trade.objects.filter(
        initiator=request.user,
        initiator_item=item_to_trade,
        receiver=receiver,
        responder_item=responder_item,
        status='initiated'
        ).exists()

        if existing_trade:
            messages.error(request, 'A trade offer for these items already exists.')
            return redirect('some_view_name')  # Redirect to a suitable view

        # Set the receiver to the owner of the item_to_trade
        receiver = item_to_trade.user

        trade = Trade(
            initiator=request.user,
            initiator_item=item_to_trade,
            receiver=receiver,
            responder_item=responder_item
        )
        print(request.POST)
        trade.save()
        messages.success(request, 'Trade offer has been sent.')
        return redirect('accounts/index.html')  # Replace with your success URL
    else:
        # If it's a GET request, just show the form
        messages.error(request, 'There was an error with your submission.')
        return render(request, 'items/initiate_trade.html', {'item_to_trade': item_to_trade, 'user_items': user_items})




@login_required
def respond_to_trade(request):
    trade_offers = Trade.objects.filter(receiver=request.user, status='initiated')
    if request.method == 'POST':
        trade_id = request.POST.get('trade_id')
        trade = get_object_or_404(Trade, id=trade_id, receiver=request.user, status='initiated')
        if 'accept' in request.POST:
            trade.status = 'completed'
            trade.save()
            
            # Logic to swap the items
            initiator_item = trade.initiator_item
            responder_item = trade.responder_item
            
            # Swap the owners
            initiator_item.user, responder_item.user = responder_item.user, initiator_item.user
            
            # Save the changes
            initiator_item.save()
            responder_item.save()
            
        elif 'decline' in request.POST:
            trade.status = 'cancelled'
            trade.save()
        return redirect('index')  # Redirect to a page showing all trade history
    return render(request, 'items/respond_to_trade.html', {'trade_offers': trade_offers})

