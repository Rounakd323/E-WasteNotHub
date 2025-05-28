from django.shortcuts import render, redirect
from .models import *
from .models import User, E_waste, Order, RefurbishedProduct, RefurbishedOrder
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def home(request):
    return render(request, 'index.html')

def register(request):
    # print("register is called")
    if request.method == "POST":
        # print("register is called after post")
        user_type = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        #username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone')
        date_of_birth = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pin_code = request.POST.get('pincode')
        company_name = request.POST.get('company_name')
        contact_person_name = request.POST.get('contact_person')

        # if User.objects.filter(username=username).exists():
        #     messages.warning(request, "Username already taken")
        #     return redirect('/register/')
        
        if User.objects.filter(email=email).exists():
            messages.warning(request, "User With the email already exists")
            return redirect('/register/')

        user = User.objects.create(
            user_type = user_type, 
            first_name = first_name,
            last_name = last_name,
            email = email,
            # username = username,
            phone_number = phone_number,
            date_of_birth = date_of_birth,
            gender = gender,
            address =  address,
            city = city,
            state = state,
            pin_code = pin_code,
            company_name = company_name,
            contact_person_name = contact_person_name,           
        )
        user.set_password(password)
        user.save()

        messages.success(request, "Registration successful")
        return redirect('/register/')
        
    return render(request, 'register.html') 

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")
        role = request.POST.get("role")
        next_url = request.GET.get("next")  # Get the ?next= URL if present

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, "Email not found")
            return redirect('/login/')

        if not user.check_password(password):
            messages.warning(request, "Invalid password")
            return redirect('/login/')

        if user.user_type != role:
            messages.warning(request, f"Invalid role selected for user: {user.user_type}")
            return redirect('/login/')

        login(request, user)
        print(f"Logged in as {user.first_name} ({user.user_type})")

        # If there's a specific next URL (like Buy Now), go there
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url:
            return redirect(next_url)

        # Otherwise go to role-based dashboard
        if user.user_type == "admin":
            return redirect(reverse('adminDashboard'))
        elif user.user_type == "seller":
            return redirect(reverse('sellerDashboard'))
        elif user.user_type == "buyer":
            return redirect(reverse('buyerDashboard'))
        elif user.user_type == "company":
            return redirect(reverse('company_dashboard'))
        else:
            return redirect(reverse('volunteerDashboard'))

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login/")
def adminDashboard(request):
    # Get only items that are pending
    pending_items = E_waste.objects.filter(listing_status='pending').order_by('-submitted_at')
    approved_count = E_waste.objects.filter(listing_status='approved').count()
    rejected_count = E_waste.objects.filter(listing_status='rejected').count()
    
    return render(request, 'dashboard.html', {
        'recent_items': pending_items,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    })

@login_required(login_url="/login/")
def reject_listing(request, item_id):
    item = get_object_or_404(E_waste, id=item_id)
    item.listing_status = 'rejected'
    item.save()
    return redirect('/admin_dashboard/')

@login_required(login_url="/login/")
def approve_listing(request, item_id):
    item = get_object_or_404(E_waste, id=item_id)
    item.listing_status = 'approved'
    item.save()
    return redirect('/admin_dashboard/')  # replace with your admin dashboard URL name

@login_required(login_url="/login/")
def approve_refurbished(request, item_id):
    item = get_object_or_404(RefurbishedProduct, id=item_id)
    item.listing_status = 'approved'
    item.save()
    return redirect('/pending_refurbished/')  # or your appropriate page

@login_required(login_url="/login/")
def reject_refurbished(request, item_id):
    item = get_object_or_404(RefurbishedProduct, id=item_id)
    item.listing_status = 'rejected'
    item.save()
    return redirect('/pending_refurbished/')  # or your appropriate page

@login_required(login_url="/login/")
def all_approvals(request):
    approved_items = E_waste.objects.filter(listing_status='approved').order_by('-submitted_at')
    approved_count = E_waste.objects.filter(listing_status='approved').count()
    rejected_count = E_waste.objects.filter(listing_status='rejected').count()
    
    return render(request, 'approvals_list.html', {
        'recent_items': approved_items,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
    })

@login_required(login_url="/login/")
def all_approvals_refurbished(request):
    approved_items = RefurbishedProduct.objects.filter(listing_status='approved').order_by('-submitted_at')
    
    return render(request, 'approvals_refurbished.html', {
        'apperoved_items': approved_items,
    })

@login_required(login_url="/login/")
def all_rejects(request):
    rejected_items = E_waste.objects.filter(listing_status='rejected').order_by('-submitted_at')
    return render(request, 'rejects_list.html', {
        'recent_items': rejected_items,
    })

@login_required(login_url="/login/")
def all_rejects_refurbished(request):
    rejected_items = RefurbishedProduct.objects.filter(listing_status='rejected').order_by('-submitted_at')

    return render(request, 'rejects_refurbished.html', {
        'rejected_items': rejected_items,
    })

def about(request):
    return render(request, 'about.html')

def privacyPolicy(request):
    return render(request, 'privacypolicy.html')

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

@login_required(login_url='/login/')
@user_passes_test(is_admin)
def company_order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'company_orders.html',
                   {
                    'orders': orders,
                   })

@login_required(login_url='/login/')
def buyer_order_list(request):
    orders = RefurbishedOrder.objects.all().order_by('-order_date')
    return render(request, 'buyer_orders.html', {
        'orders': orders,
    })

# @login_required(login_url='/login/')
# def assign_driver(request, order_id):
#     order = get_object_or_404(Order, id=order_id)

#     # Prevent accessing cancelled orders
#     if order.status == 'cancelled':
#         messages.error(request, "Cannot assign a driver to a cancelled order.")
#         return redirect('/company_orders_admin/')  # Replace with your actual order list view
#     if order.driver:
#         messages.warning(request, f"A driver is already assigned to this order: {order.driver.get_full_name()}")
#         # return redirect(f'/assign_driver/{order_id}/')
#         return redirect('/company_orders_admin/')

#     drivers = User.objects.filter(user_type='volunteer')

#     if request.method == 'POST':
#         driver_id = request.POST.get('driver_id')
#         pickup_datetime = request.POST.get('pickup_datetime')
#         delivery_datetime = request.POST.get('delivery_datetime')

#         driver = get_object_or_404(User, id=driver_id, user_type='volunteer')

#         # Only assign a driver if no driver has been assigned yet.
#         if not order.driver:
#             order.driver = driver
#             order.pickup_datetime = parse_datetime(pickup_datetime)
#             order.delivery_datetime = parse_datetime(delivery_datetime)
#             order.status = 'shipped'
#             order.save()
#             messages.success(request, f"Assigned driver {driver.get_full_name()} with pickup and delivery schedule.")
#         else:
#             messages.warning(request, "A driver has already been assigned to this order.")

#         return redirect(f'/assign_driver/{order_id}/')

#     return render(request, 'assign_driver.html', {
#         'order': order,
#         'drivers': drivers,
#     })

@login_required(login_url='/login/')
def assign_driver(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == 'cancelled':
        messages.error(request, "Cannot assign a driver to a cancelled order.")
        return redirect('/company_orders_admin/')

    drivers = User.objects.filter(user_type='volunteer')

    if request.method == 'POST':
        if order.driver:
            messages.warning(request, f"A driver is already assigned: {order.driver.get_full_name()}")
            return redirect('/company_orders_admin/')

        driver_id = request.POST.get('driver_id')
        pickup_datetime = request.POST.get('pickup_datetime')
        delivery_datetime = request.POST.get('delivery_datetime')

        driver = get_object_or_404(User, id=driver_id, user_type='volunteer')

        order.driver = driver
        order.pickup_datetime = parse_datetime(pickup_datetime)
        order.delivery_datetime = parse_datetime(delivery_datetime)
        order.status = 'shipped'
        order.save()

        messages.success(request, f"Assigned driver {driver.get_full_name()} successfully.")
        return redirect('/company_orders_admin/')  # ✅ Redirect to a different view

    if order.driver:
        messages.warning(request, f"A driver is already assigned: {order.driver.get_full_name()}")
        return redirect('/company_orders_admin/')

    return render(request, 'assign_driver.html', {
        'order': order,
        'drivers': drivers,
    })


# @login_required(login_url='/login/')
# def assign_driver_refurbished(request, order_id):
#     order = get_object_or_404(RefurbishedOrder, id=order_id)

#     if order.status == 'cancelled':
#         messages.error(request, "Cannot assign a driver to a cancelled order.")
#         return redirect('/buyer_orders_admin/')

#     if order.driver:
#         messages.warning(request, f"A driver is already assigned: {order.driver.get_full_name()}")
#         return redirect('/buyer_orders_admin/')

#     drivers = User.objects.filter(user_type='volunteer')

#     if request.method == 'POST':
#         driver_id = request.POST.get('driver_id')
#         pickup_datetime = request.POST.get('pickup_datetime')
#         delivery_datetime = request.POST.get('delivery_datetime')

#         driver = get_object_or_404(User, id=driver_id, user_type='volunteer')

#         if not order.driver:
#             order.driver = driver
#             order.pickup_datetime = parse_datetime(pickup_datetime)
#             order.delivery_datetime = parse_datetime(delivery_datetime)
#             order.status = 'shipped'
#             order.save()
#             messages.success(request, f"Assigned driver {driver.get_full_name()} successfully.")

#         return redirect(f'/assign_driver_refurbished/{order_id}/')

#     return render(request, 'assign_driver.html', {
#         'order': order,
#         'drivers': drivers,
#     })

@login_required(login_url='/login/')
def assign_driver_refurbished(request, order_id):
    order = get_object_or_404(RefurbishedOrder, id=order_id)

    if order.status == 'cancelled':
        messages.error(request, "Cannot assign a driver to a cancelled order.")
        return redirect('/buyer_orders_admin/')

    drivers = User.objects.filter(user_type='volunteer')

    if request.method == 'POST':
        if order.driver:
            messages.warning(request, f"A driver is already assigned: {order.driver.get_full_name()}")
            return redirect('/buyer_orders_admin/')

        driver_id = request.POST.get('driver_id')
        pickup_datetime = request.POST.get('pickup_datetime')
        delivery_datetime = request.POST.get('delivery_datetime')

        driver = get_object_or_404(User, id=driver_id, user_type='volunteer')

        order.driver = driver
        order.pickup_datetime = parse_datetime(pickup_datetime)
        order.delivery_datetime = parse_datetime(delivery_datetime)
        order.status = 'shipped'
        order.save()

        messages.success(request, f"Assigned driver {driver.get_full_name()} successfully.")
        return redirect('/buyer_orders_admin/')  # ✅ Redirect to a different view

    if order.driver:
        messages.warning(request, f"A driver is already assigned: {order.driver.get_full_name()}")
        return redirect('/buyer_orders_admin/')

    return render(request, 'assign_driver.html', {
        'order': order,
        'drivers': drivers,
    })

@login_required(login_url="/login/")
def pending_refurbished_list(request):
    pending_items = RefurbishedProduct.objects.filter(listing_status='pending')
    return render(request, 'pending_refurbished.html', {'pending_items': pending_items})

@login_required(login_url="/login/")
def ewaste_details_to_admin(request, item_id):
    # Do not filter by seller — admins should access all items
    item = get_object_or_404(E_waste, id=item_id)
    
    return render(request, 'ewaste_details_to_admin.html', {
        'item': item,
    })

@login_required(login_url="/login/")
def ewaste_details_to_admin2(request, item_id):
    # Do not filter by seller — admins should access all items
    item = get_object_or_404(E_waste, id=item_id)
    
    return render(request, 'ewaste_details_to_admin2.html', {
        'item': item,
    })

@login_required(login_url="/login/")
def refurbished_details_to_admin(request, item_id):
    # Do not filter by seller — admins should access all items
    item = get_object_or_404(RefurbishedProduct, id=item_id)
    
    return render(request, 'refurbished_product_details_to_admin.html', {
        'item': item,
    })

@login_required(login_url="/login/")
def refurbished_details_to_admin2(request, item_id):
    # Do not filter by seller — admins should access all items
    item = get_object_or_404(RefurbishedProduct, id=item_id)
    
    return render(request, 'refurbished_product_details_to_admin2.html', {
        'item': item,
    })

def test_password_reset_template(request):
    return render(request, 'registration/password_reset_form.html')

# @login_required
# def give_feedback(request):
#     if request.method == 'POST':
#         feedback_text = request.POST.get('feedback_text')
#         if feedback_text:
#             # Auto-detect user_type here from logged-in user
#             user_type = request.user.user_type  
#             Feedback.objects.create(user=request.user, user_type=user_type, text=feedback_text)
#             return render(request, 'feedback.html', {'message': 'Thanks for your feedback!'})
#         else:
#             return render(request, 'feedback.html', {'error': 'Please enter feedback before submitting.'})
#     return render(request, 'feedback.html')

# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def give_feedback(request):
    # Prevent admins from giving feedback
    if request.user.user_type == 'admin':
        return render(request, 'feedback.html', {'error': 'Admins are not allowed to give feedback.'})


    if request.method == 'POST':
        feedback_text = request.POST.get('feedback_text')
        if feedback_text:
            user_type = request.user.user_type
            Feedback.objects.create(user=request.user, user_type=user_type, text=feedback_text)
            return render(request, 'feedback.html', {'message': 'Thanks for your feedback!'})
        else:
            return render(request, 'feedback.html', {'error': 'Please enter feedback before submitting.'})
    
    return render(request, 'feedback.html')


def feedback_page(request):
    feedbacks = Feedback.objects.all().order_by('-id')  # newest first
    return render(request, 'feedback_page.html', {'feedbacks': feedbacks})