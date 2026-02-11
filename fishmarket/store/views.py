from django.shortcuts import render, redirect
from .models import Fish, Order, OrderItem
from .forms import CheckoutForm

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




def remove_from_cart(request, fish_id):
    cart = request.session.get('cart', {})
    if str(fish_id) in cart:
        del cart[str(fish_id)]
    request.session['cart'] = cart
    return redirect('cart')


def increase_quantity(request, fish_id):
    cart = request.session.get('cart', {})
    if str(fish_id) in cart:
        cart[str(fish_id)] += 1
    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, fish_id):
    cart = request.session.get('cart', {})
    if str(fish_id) in cart:
        cart[str(fish_id)] -= 1

        if cart[str(fish_id)] <= 0:
            del cart[str(fish_id)]

    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    cart_items = []
    total = 0

    # calculate cart data
    for fish_id, quantity in cart.items():
        fish = Fish.objects.get(id=fish_id)
        item_total = fish.price * quantity
        total += item_total

        cart_items.append({
            'fish': fish,
            'quantity': quantity,
            'total_price': item_total
        })

    form = CheckoutForm()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total
            order.save()

            # Save Order Items
            for fish_id, quantity in cart.items():
                fish = Fish.objects.get(id=fish_id)

                OrderItem.objects.create(
                    order=order,
                    fish_name=fish.name,
                    quantity=quantity,
                    price=fish.price
                )

            request.session['last_total'] = float(total)



            # clear cart after order
            request.session['cart'] = {}

            return redirect('checkout_success')

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })

def checkout_success(request):
    total = request.session.get('last_total', 0)
    return render(request, 'checkout_success.html', {'total': total})




