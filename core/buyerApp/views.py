from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from adminApp.models import RefurbishedProduct, RefurbishedOrder
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url="/login/")
def buyerDashboard(request):
    return render(request, 'dashboard_buyer.html')

def browseProduct(request):
    approved_items = RefurbishedProduct.objects.filter(listing_status='approved').order_by('-submitted_at')
    return render(request, 'browse_product.html', {
        'approved_items': approved_items
    })

@login_required(login_url="/login/")
def browseProductBuy(request):
    approved_items = RefurbishedProduct.objects.filter(listing_status='approved').order_by('-submitted_at')
    return render(request, 'browse_product_buy.html', {
        'approved_items': approved_items
    })


def product_detail(request, item_id):
    refurbsh_item = get_object_or_404(RefurbishedProduct, id=item_id, listing_status='approved')

    return render(request, 'product_details.html', {
        'item': refurbsh_item,
    })

@login_required(login_url="/login/")
def product_detail_buy(request, item_id):
    refurbsh_item = get_object_or_404(RefurbishedProduct, id=item_id, listing_status='approved')

    return render(request, 'product_details_buy.html', {
        'item': refurbsh_item,
    })

@login_required(login_url='/login/')
def payment_buyer(request, item_id):
    item = get_object_or_404(RefurbishedProduct, id=item_id)
    return render(request, 'payment_buyer.html', {'item': item})

@login_required(login_url='/login/')
def make_payment_buyer(request, item_id):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        item = get_object_or_404(RefurbishedProduct, id=item_id)

        # Create order
        RefurbishedOrder.objects.create(
            buyer=request.user,
            product=item,
            payment_method=payment_method,
            total_price=item.price,
            status='processing'
        )

        return redirect('/order_buyer/')  # Redirect to buyer order list page

    return redirect('home')

@login_required(login_url='/login/')
def order_buyer(request):
    orders = RefurbishedOrder.objects.filter(buyer=request.user).order_by('-order_date')
    context = {
        'orders': orders,
        'no_orders': not orders.exists()
    }
    return render(request, 'order_buyer.html', context)