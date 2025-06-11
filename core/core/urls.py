"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from adminApp.views import *
from sellerApp.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import  staticfiles_urlpatterns
from buyerApp.views import *
from volunteerApp.views import *
from companyApp.views import *
from django.contrib.auth import views as auth_views
from adminApp import views as admin_views

urlpatterns = [
    path('', home, name="home"),
    path('contact/', contact, name="contact"),
    path('showfeedback',showfeedback,name='showfeedback'),
    path('register/', register, name="register"),
    path('login/', user_login, name="user_login"),
    path('feedback/',give_feedback, name='give_feedback'),
    path('feedbacks/',feedback_page, name='feedback_page'),
    path('logout/', user_logout, name="user_logout"),
    path('admin_dashboard/', adminDashboard, name="adminDashboard"),
    path('listing/<int:item_id>/approve/', approve_listing, name='approve_listing'),
    path('listing/<int:item_id>/reject/', reject_listing, name='reject_listing'),
    path('all_approvals/', all_approvals, name='all_approvals'),
    path('refurbished_approvals/', all_approvals_refurbished, name='refurbished_approvals'),
    path('all_rejects/', all_rejects, name='all_rejects'),
    path('refurbished_rejects/', all_rejects_refurbished, name='refurbished_rejects'),
    path('about/', about, name="about"),
    path('privacy_policy/', privacyPolicy, name="privacyPolicy"),
    path('company_orders_admin/', company_order_list, name='company_order_list'),
    path('buyer_orders_admin/', buyer_order_list, name='buyer_order_list'),
    path('assign_driver/<int:order_id>/', assign_driver, name='assign_driver'),
    path('assign_driver_refurbished/<int:order_id>/', assign_driver_refurbished, name='assign_driver_refurbished'),
    path('pending_refurbished/', pending_refurbished_list, name='pending_refurbished'),
    path('approve_refurbished/<int:item_id>/', approve_refurbished, name='approve_refurbished'),
    path('reject_refurbished/<int:item_id>/', reject_refurbished, name='reject_refurbished'),
    path('ewaste_details_to_admin/<int:item_id>/', ewaste_details_to_admin, name='ewaste_details_to_admin'),
    path('refurbished_details_to_admin/<int:item_id>/', refurbished_details_to_admin, name='refurbished_details_to_admin'),
    path('ewaste_details_to_admin_view/<int:item_id>/', ewaste_details_to_admin2, name='ewaste_details_to_admin2'),
    path('refurbished_details_to_admin_view/<int:item_id>/', refurbished_details_to_admin2, name='refurbished_details_to_admin2'),

    path('seller_dashboard/', sellerDashboard, name="sellerDashboard"),
    path('post_waste/', post_waste, name="post_waste"),
    path('all_listings/', all_listings, name="all_listings"),
    path('all_orders_seller/', all_orders_seller, name="all_orders_seller"),
    path('ewaste_details_seller/<int:item_id>/', ewaste_details_seller, name="ewaste_details_seller"),

    path('buyer_dashboard/', buyerDashboard,name="buyerDashboard"),
    path('browseProduct/', browseProduct,name="browseProduct"),
    path('browseProductBuy/', browseProductBuy,name="browseProductBuy"),
    path('product/<int:item_id>/', product_detail, name='product_detail'),
    path('product_buy/<int:item_id>/', product_detail_buy, name='product_detail_buy'),
    path('payment_buyer/<int:item_id>/', payment_buyer, name='payment_buyer'),
    path('order_buyer/', order_buyer, name='order_buyer'),
    path('make_payment_buyer/<int:item_id>/', make_payment_buyer, name='make_payment_buyer'),

    path('volunteer_dashboard/',volunteerDashboard,name="volunteerDashboard"),
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('update_refurbished_order_status/<int:order_id>/', update_refurbished_order_status, name='update_refurbished_order_status'),

    path('company_dashboard/', company_dashboard,name="company_dashboard"),
    path('post_refurbished/', post_refurbished,name="post_refurbished"),
    path('browse_E_Waste/', browse_E_Waste,name="browse_E_Waste"),
    path('ewaste/<int:item_id>/', ewaste_detail, name='ewaste_detail'),
    path('company_cart/', company_cart, name='company_cart'),
    path('add_to_cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    # path('buy_now/<int:item_id>/', buy_now, name='buy_now'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('payment/<int:item_id>/', payment, name='payment'),
    path('make_payment/<int:item_id>/', make_payment, name='make_payment'),
    path('order_company/', order_company, name='order_company'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order'),
    path('order_to_company/', order_to_company, name="order_to_company"),
    path('refurbished_details_company/<int:item_id>/', refurbished_details_company, name="refurbished_details_company"),
        
    #urls for pass recovery
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # path('test-reset-form/', admin_views.test_password_reset_template, name='test_reset_form'),

    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT
    )
urlpatterns += staticfiles_urlpatterns()
