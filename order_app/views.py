from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render

from order_app.models import Cart, Order
from shop_app.models import Product

from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def add_to_cart(request,pk):
    item = get_object_or_404(Product, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchase=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, 'This item quantity in updated.')
            return redirect('shop_app:home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(request, 'This Item was added to your cart.')
            return redirect('shop_app:home')
    else:
        order = Order(user=request.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(request, 'This Item is added to your cart.')
        return redirect('shop_app:home')

@login_required
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchase = False)
    orders = Order.objects.filter(user=request.user, ordered = False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(request, 'order_app/cart.html', context={'carts': carts, 'order': order})
    else:
        messages.warning(request, "you don't have any item in your cart.")
        return redirect('shop_app:home')



@login_required
def remove_cart_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user= request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user= request.user, purchase = False)
            order_item = order_item[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request,"This item remove from your cart.")
            return redirect('order_app:cart')
        else:
            messages.warning(request,"This item was not in your cart.")
            return redirect('shop_app:home')
    else:
        messages.info(request, "Your Haven't any Active order.")
        return redirect('shop_app:home')

@login_required
def item_increase(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user = request.user, purchase = False)
            order_item = order_item[0]
            if order_item.quantity >=1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f'{item.name} quantity has been updated.')
                return redirect('order_app:cart')
        else:
            messages.warning(request, f"{item.name} is not in your cart")
            return redirect('shop_app:home')
    else:
        messages.info(request, "you don't have an active order")
        return redirect('shop_app:home')

@login_required
def item_decrease(request,pk):
    item = get_object_or_404(Product, pk = pk)
    order_qs = Order.objects.filter(user=request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user = request.user, purchase = False)
            order_item = order_item[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, 'quantity has been updated.')
                return redirect('order_app:cart')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f'{item.name} has been removed from your cart')
                return redirect('order_app:cart')
        else:
            messages.warning(request, f"{item.name} is not in your cart")
            return redirect('shop_app:home')
    else:
        messages.info(request, "you don't have an active order")
        return redirect('shop_app:home')
