from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from adminApp.models import Order, RefurbishedOrder
from django.utils import timezone
from itertools import chain
from django.utils.timezone import now

# Create your views here.
@login_required(login_url="/login/")
def volunteerDashboard(request):
    # E-Waste Orders
    ewaste_orders = Order.objects.filter(driver=request.user).select_related('e_waste_item__seller', 'company')
    for order in ewaste_orders:
        order.order_type = 'ewaste'

    # Refurbished Product Orders
    refurbished_orders = RefurbishedOrder.objects.filter(driver=request.user).select_related('product__company', 'buyer')
    for order in refurbished_orders:
        order.order_type = 'refurbished'

    # Combine and sort by pickup time
    combined_orders = sorted(
        chain(ewaste_orders, refurbished_orders),
        key=lambda x: x.pickup_datetime or now()
    )

    return render(request, 'dashboard_volunteer.html', {'orders': combined_orders})

@login_required(login_url="/login/")
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, driver=request.user)
        status = request.POST.get('status')
        if status in ['shipped', 'on the way', 'delivered']:
            order.status = status
            if status == 'delivered':
                order.delivery_datetime = timezone.now()
            order.save()
    return redirect('/volunteer_dashboard/')

@login_required(login_url="/login/")
def update_refurbished_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(RefurbishedOrder, id=order_id, driver=request.user)
        status = request.POST.get('status')
        if status in ['shipped', 'on the way', 'delivered']:
            order.status = status
            if status == 'delivered':
                order.delivery_datetime = timezone.now()
            order.save()
    return redirect('/volunteer_dashboard/')
