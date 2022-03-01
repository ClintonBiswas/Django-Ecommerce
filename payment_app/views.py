from django.shortcuts import render, HttpResponseRedirect

from order_app.models import Order
from payment_app.models import BillingAddress
from payment_app.forms import BillingForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def check_out(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)
    saved_address = saved_address[0]
    form = BillingForm(instance=saved_address)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            form = BillingForm(instance=saved_address)
            messages.info(request, "Shipping Address Is Saved")
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    diction = {'billing_form': form, 'order_items': order_items, 'order_total': order_total, 'saved_address':saved_address}
    return render(request, 'payment_app/check_out.html', context=diction)
