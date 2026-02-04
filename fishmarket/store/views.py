from django.shortcuts import render, redirect
from .models import Fish

def home(request):
    fishes = Fish.objects.all()
    return render(request, 'home.html', {'fishes': fishes})


def shop(request):
    fishes = Fish.objects.all()
    return render(request, 'shop.html', {'fishes': fishes})


def add_to_cart(request, fish_id):
    cart = request.session.get('cart', {})

    if str(fish_id) in cart:
        cart[str(fish_id)] += 1
    else:
        cart[str(fish_id)] = 1

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for fish_id, quantity in cart.items():
        fish = Fish.objects.get(id=fish_id)
        item_total = fish.price * quantity
        total += item_total
        cart_items.append({
            'fish': fish,
            'quantity': quantity,
            'total_price': item_total
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def login_view(request):
    return render(request, 'login.html')
