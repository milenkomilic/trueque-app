from gettext import translation
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Item, Trade, CustomUser
from .forms import CustomUserCreationForm, ItemForm
from .forms import CustomUserEditForm
from django.db.models import Q, F, Max, OuterRef, Subquery
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

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
    items_list = Item.objects.exclude(
        (Q(user_id=F('trade__receiver_id')) | Q(user_id=F('trade__initiator_id'))) &
        (Q(trade__status='cancelled') | Q(trade__status='initiated') | Q(trade__status='accepted'))
    )

    items_list = items_list.exclude(Q(user=request.user))

    paginator = Paginator(items_list, 4)

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


def my_items(request):
    items = Item.objects.filter(user=request.user)
    paginator = Paginator(items, 4)

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'accounts/my_items.html', {'items': items, 'page_obj': items})


@login_required
def initiate_trade(request, item_id):
    item_to_trade = get_object_or_404(Item, id=item_id, active=True)
    user_items = Item.objects.filter(user=request.user, active=True)
    
    if request.method == 'POST':
        initiator_item = get_object_or_404(Item, id=request.POST.get('responder_item'), user=request.user, active=True)
        receiver = item_to_trade.user

        existing_trade = Trade.objects.filter(
        initiator=initiator_item.user,
        initiator_item=initiator_item,
        receiver=receiver,
        responder_item=item_to_trade
        ).exists()

        if existing_trade:
            messages.error(request, 'A trade offer for these items already exists.')
            return redirect('initiate_trade', item_id=item_id)

        trade = Trade(
            initiator=request.user,
            initiator_item=initiator_item,
            receiver=receiver,
            responder_item=item_to_trade
        )
        trade.save()

        item_to_trade.trade = trade
        initiator_item.trade = trade
        item_to_trade.save()
        initiator_item.save()

        messages.success(request, 'Trade offer has been sent.')
        return redirect('initiate_trade', item_id=item_id)
    
    return render(request, 'items/initiate_trade.html', {'item_to_trade': item_to_trade, 'user_items': user_items})


@login_required
def respond_to_trade(request):
    if request.method == 'POST':
        trade_id = request.POST.get('trade_id')
        trade = get_object_or_404(Trade, id=trade_id)
        if 'accept' in request.POST:
            trade.status = 'accepted' if trade.status == 'initiated' else 'completed'
            trade.receiver = trade.initiator
            trade.initiator = trade.receiver
            trade.save()

            if trade.status == 'completed':
                initiator_item = trade.initiator_item
                responder_item = trade.responder_item
                initiator_item.user, responder_item.user = responder_item.user, initiator_item.user
                messages.success(request, 'Trade accepted successfully.')
                initiator_item.save()
                responder_item.save()

                user_trades = Trade.objects.filter(
                    Q(receiver=request.user) &
                    (Q(initiator_item=initiator_item) & Q(responder_item=responder_item)) &
                    (Q(status='initiated') | Q(status='accepted'))
                )

                user_trades.update(status='cancelled')
        elif 'decline' in request.POST:
            trade.status = 'cancelled'
            messages.info(request, 'Trade declined.')
            trade.save()
        return redirect('respond_to_trade')
    
    trade_offers = Trade.objects.filter(
        Q(receiver=request.user) & 
        (Q(status='initiated') | Q(status='accepted'))
    )
    return render(request, 'items/respond_to_trade.html', {'trade_offers': trade_offers})


@login_required
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    elif request.method == 'GET':
        form = CustomUserEditForm(instance=request.user)
        return render(request, 'accounts/edit_profile.html', {'form': form})

    return HttpResponse("Method Not Allowed", status=405)


@csrf_exempt
@login_required
def update_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')
        active = request.POST.get('active') == 'true'

        # Encuentra y actualiza el ítem
        item = get_object_or_404(Item, id=item_id, user=request.user)
        item.title = title
        item.price = price
        item.description = description
        item.active = active
        item.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
@login_required
def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id, user=request.user)  # Asegurar que el ítem pertenece al usuario

        item.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)