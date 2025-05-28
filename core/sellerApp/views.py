from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from adminApp.models import User, E_waste, Order, EWasteImage
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url="/login/")
def sellerDashboard(request):
    user = request.user
    total_listings = E_waste.objects.filter(seller=user).count()
    recent_items = E_waste.objects.filter(seller=user).order_by('-submitted_at')[:3]
    # recent_items = E_waste.objects.filter(seller=user).order_by('-submitted_at')[:3]
    return render(request, 'dashboard_seller.html', {
        'recent_items': recent_items,
        'total_listings': total_listings,
    })

@login_required(login_url="/login/")
def all_listings(request):
    user = request.user
    seller_items = E_waste.objects.filter(seller=user).order_by('-submitted_at')
    return render(request, 'all_listings.html', {'items': seller_items})

@login_required(login_url="/login/")
def post_waste(request):
    if request.method == "POST":
        product_name = request.POST.get('name')
        product_condition = request.POST.get('condition')
        description = request.POST.get('description') 
        images = request.FILES.getlist('images')  # use getlist to get all uploaded files
        product_price = request.POST.get('price')

        e_waste = E_waste.objects.create(
            seller=request.user,
            product_name=product_name,
            product_condition=product_condition,
            description=description,
            product_price=product_price,
        )

        for image in images:
            EWasteImage.objects.create(e_waste=e_waste, image=image)

        messages.success(request, "Your product has been uploaded.")
        return redirect('/post_waste/')
    
    return render(request, 'post_waste.html')

@login_required(login_url='/login/')
def all_orders_seller(request):
    # Filter orders related to e-waste items uploaded by the current seller
    seller = request.user
    orders = Order.objects.filter(e_waste_item__seller=seller).select_related(
        'e_waste_item', 'company', 'driver'
    ).order_by('-id')  # optional: order by latest

    return render(request, 'all_orders_to_seller.html', {
        'orders': orders
    })

@login_required(login_url="/login/")
def ewaste_details_seller(request, item_id):
    item = get_object_or_404(E_waste, id=item_id, seller=request.user)
    company_address = request.user  # or however you're storing company info
    
    return render(request, 'ewaste_details_seller.html', {
        'item': item,
        'company_address': company_address,
    })


