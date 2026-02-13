from django.shortcuts import render, redirect
from .models import Fish, FishCategory, Order, OrderItem
from django.contrib import messages
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


def home(request):
    fishes = Fish.objects.all()
    return render(request, 'home.html', {'fishes': fishes})


def shop(request):
    fishes = Fish.objects.all()

    search_query = request.GET.get('search')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_query:
        fishes = fishes.filter(name__icontains=search_query)

    if category:
        fishes = fishes.filter(category__id=category)

    if min_price:
        fishes = fishes.filter(price__gte=min_price)

    if max_price:
        fishes = fishes.filter(price__lte=max_price)

    categories = FishCategory.objects.all()

    return render(request, 'shop.html', {
        'fishes': fishes,
        'categories': categories
    })



def add_to_cart(request, fish_id):
    cart = request.session.get('cart', {})

    fish = Fish.objects.get(id=fish_id)

    # current quantity already in cart
    current_qty = cart.get(str(fish_id), 0)

    # stock check BEFORE adding
    if fish.stock <= 0:
        messages.error(request, "Item is out of stock")
        return redirect('shop')

    if current_qty >= fish.stock:
        messages.error(request, f"Only {fish.stock} items available in stock")
        return redirect('shop')

    # safe to add
    cart[str(fish_id)] = current_qty + 1
    request.session['cart'] = cart

    messages.success(request, f"{fish.name} added to cart 🛒")
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


            for item in cart_items:
              fish = item.fish
              qty = item.quantity

            if fish.stock >= qty:
              fish.stock -= qty
              fish.save()




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


def orders(request):
    return render(request, 'orders.html')


