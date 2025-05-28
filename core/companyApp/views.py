from django.shortcuts import render, redirect
from adminApp.models import RefurbishedProduct
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from adminApp.models import E_waste, CompanyCart, Order, RefurbishedOrder, RefurbishedProduct, RefurbishedProductImage
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url='/login/')
def company_dashboard(request):
    # Get only the products posted by the currently logged-in company/user
    recent_items = RefurbishedProduct.objects.filter(company=request.user).order_by('-submitted_at')

    return render(request, 'company_dashboard.html', {
        'recent_items': recent_items
    })

@login_required(login_url='/login/')
def post_refurbished(request):
    if request.method == "POST":
        category = request.POST.get('category')
        product_name = request.POST.get('product_name')
        images = request.FILES.getlist('images')
        price = request.POST.get('price')
        description = request.POST.get('description')
        warranty = request.POST.get('warranty')

        if category == "laptop":
            ram = request.POST.get('laptop_ram')
            storage = request.POST.get('laptop_storage')
            processor = request.POST.get('laptop_processor')
        elif category == "mobile":
            ram = request.POST.get('mobile_ram')
            storage = request.POST.get('mobile_storage')
            processor = request.POST.get('mobile_processor')
        else:
            ram = storage = processor = None

        display_size = request.POST.get('display_size')

        if category == "fridge":
            capacity = request.POST.get('fridge_capacity')
            energy_rating = request.POST.get('fridge_energy_rating')
        elif category == "ac":
            capacity = request.POST.get('ac_capacity')
            energy_rating = request.POST.get('ac_energy_rating')
        else:
            capacity = energy_rating = None

        door = request.POST.get('door')
        extra_info = request.POST.get('extra_info')

        # Save product without image
        refurbished = RefurbishedProduct.objects.create(
            company=request.user,
            category=category,
            product_name=product_name,
            price=price,
            description=description,
            warranty=warranty,
            ram=ram,
            storage=storage,
            processor=processor,
            display_size=display_size,
            capacity=capacity,
            door=door,
            energy_rating=energy_rating,
            extra_info=extra_info,
        )

        # Save all images
        for img in images:
            RefurbishedProductImage.objects.create(product=refurbished, image=img)

        messages.success(request, "Your product has been uploaded.")
        return redirect('/post_refurbished/') 

    return render(request, 'post_refurbished.html')

# def browse_E_Waste(request):
#     return render(request, 'browse_e_waste.html')

@login_required(login_url='/login/')
def browse_E_Waste(request):
    # Fetch all approved e-waste listings
    approved_items = E_waste.objects.filter(listing_status='approved').order_by('-submitted_at')

    return render(request, 'browse_e_waste.html', {
        'approved_items': approved_items
    })

@login_required(login_url='/login/')
def ewaste_detail(request, item_id):
    ewaste_item = get_object_or_404(E_waste, id=item_id, listing_status='approved')

    # Check if the user is a company to fetch address
    if request.user.user_type == 'company':
        company_address = {
            'address': request.user.address,
            'city': request.user.city,
            'state': request.user.state,
            'pin_code': request.user.pin_code,
            'company_name': request.user.company_name,
        }
    else:
        company_address = None  # Or you can handle unauthorized access

    return render(request, 'ewaste_detail.html', {
        'item': ewaste_item,
        'company_address': company_address
    })

@login_required(login_url='/login/')
def company_cart(request):
    items = CompanyCart.objects.filter(company=request.user)
    return render(request, 'cart.html', {'items': items})

@login_required(login_url='/login/')
def add_to_cart(request, item_id):
    if request.user.is_authenticated and request.user.user_type == 'company':
        e_waste_item = get_object_or_404(E_waste, id=item_id, listing_status='approved')
        
        # Check if already in cart (optional to avoid duplicates)
        existing_item = CompanyCart.objects.filter(company=request.user, e_waste_item=e_waste_item)
        if not existing_item.exists():
            CompanyCart.objects.create(
                company=request.user, e_waste_item=e_waste_item
            )
    return redirect('/company_cart/')  # Replace with your cart page URL name

# @login_required(login_url='/login/')
# def buy_now(request, item_id):
#     if request.user.is_authenticated and request.user.user_type == 'company':
#         e_waste_item = get_object_or_404(E_waste, id=item_id, listing_status='approved')
#         # Directly create an order here (if you have an Order model)
#         # For now just add to cart then redirect to checkout
#         cart_item = CompanyCart.objects.create(company=request.user, e_waste_item=e_waste_item)
#         return redirect('checkout_page')  # Create a checkout page/view later
#     return redirect('login')  # If not logged in

@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CompanyCart, id=item_id, company=request.user)
        cart_item.delete()
    return redirect('/company_cart/')  # redirect back to cart

@login_required(login_url='/login/')
def payment(request, item_id):
    item = get_object_or_404(E_waste, id=item_id)
    return render(request, 'payment_company.html', {'item': item})

@login_required(login_url='/login/')
def make_payment(request, item_id):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        item = get_object_or_404(E_waste, id=item_id)

        # Create order
        Order.objects.create(
            company=request.user,
            e_waste_item=item,
            payment_method=payment_method,
            total_price=item.product_price,
            status='processing'  # default status
        )

        return redirect('/order_company/')  # Redirect to company order list page

    return redirect('home')


@login_required(login_url='/login/')
def order_company(request):
    orders = Order.objects.filter(company=request.user).order_by('-order_date')
    context = {
        'orders': orders,
        'no_orders': not orders.exists()
    }
    return render(request, 'order_company.html', context)

@login_required(login_url='/login/')
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, company=request.user)
    if order.status in ['processing', 'shipped']:  # only allow cancellation before delivery
        order.status = 'cancelled'
        order.save()
        # messages.success(request, "Order cancelled successfully.")
    else:
        pass
        # messages.error(request, "This order cannot be cancelled.")
    return redirect('order_company')

@login_required(login_url='/login/')
def order_to_company(request):
    orders = RefurbishedOrder.objects.filter(product__company=request.user).select_related('product', 'buyer', 'driver')
    
    return render(request, 'order_to_company.html', {'orders': orders})

@login_required(login_url="/login/")
def refurbished_details_company(request, item_id):
    item = get_object_or_404(RefurbishedProduct, id=item_id, company=request.user)
    company_address = request.user  # or however you're storing company info
    
    return render(request, 'refurbished_details_company.html', {
        'item': item,
        'company_address': company_address,
    })
    



