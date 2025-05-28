from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    username = None  # Remove default username
    email = models.EmailField(unique=True)  # Use email as login field

    USER_TYPE_CHOICES = [
    ('seller', 'Seller'),
    ('buyer', 'Buyer'),
    ('volunteer', 'Volunteer'),
    ('admin', 'Admin'),
    ('company', 'Company')
    ]
    GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    ]

    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES,
        null=True,  # Allow NULL in the database
        blank=True,  # Allow empty value in forms/admin
    )
    
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True) # Date Field
    gender = models.CharField(max_length=15,choices=GENDER_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    pin_code = models.CharField(max_length=30, null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    contact_person_name = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Or any fields you want during createsuperuser


class E_waste(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_condition = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    submitted_at = models.DateTimeField(default=timezone.now)

    LISTING_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    listing_status = models.CharField(max_length=20, choices=LISTING_STATUS, default='pending')

class EWasteImage(models.Model):
    e_waste = models.ForeignKey(E_waste, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='seller_products/')

class RefurbishedProduct(models.Model):
    CATEGORY_CHOICES = [
        ('laptop', 'Laptop'),
        ('mobile', 'Mobile'),
        ('fridge', 'Fridge'),
        ('ac', 'AC'),
        ('other', 'Other'),
    ]

    company = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='refurbished_products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    warranty = models.CharField(max_length=100, blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)
    listing_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )

    # Laptop / Mobile Fields
    ram = models.CharField(max_length=50, blank=True, null=True)
    storage = models.CharField(max_length=100, blank=True, null=True)
    processor = models.CharField(max_length=100, blank=True, null=True)
    display_size = models.CharField(max_length=50, blank=True, null=True)  # Only for laptop

    # Fridge / AC Fields
    capacity = models.CharField(max_length=50, blank=True, null=True)
    door = models.CharField(max_length=50, blank=True, null=True)  # Only for fridge
    energy_rating = models.CharField(max_length=50, blank=True, null=True)

    # Others
    extra_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product_name} ({self.category})"
    
class RefurbishedProductImage(models.Model):
    product = models.ForeignKey(RefurbishedProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='refurbished_products/')

class CompanyCart(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'company'})
    e_waste_item = models.ForeignKey(E_waste, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('in_cart', 'In Cart'), ('purchased', 'Purchased')], default='in_cart')

    def __str__(self):
        return f"{self.company.company_name} - {self.e_waste_item.product_name}"

class Order(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company_orders')
    e_waste_item = models.ForeignKey(E_waste, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    ORDER_STATUS = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('on the way', 'On the way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='processing')

    # Add this field:
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'volunteer'},
        related_name='driver_orders',
    )
    pickup_datetime = models.DateTimeField(null=True, blank=True)
    delivery_datetime = models.DateTimeField(null=True, blank=True)

class RefurbishedOrder(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'buyer'})
    product = models.ForeignKey(RefurbishedProduct, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    ORDER_STATUS = [
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('on the way', 'On the way'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='processing')

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_type': 'volunteer'},
        related_name='refurbished_driver_orders',
    )
    pickup_datetime = models.DateTimeField(null=True, blank=True)
    delivery_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.product_name} for {self.buyer.username}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=User.USER_TYPE_CHOICES, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} at {self.created_at}"
