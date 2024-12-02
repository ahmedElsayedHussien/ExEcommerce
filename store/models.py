from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, help_text='Recommended size: 200x200 pixels')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_start_date = models.DateTimeField(null=True, blank=True)
    discount_end_date = models.DateTimeField(null=True, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='products',
        null=True,
        blank=True,
        verbose_name='Product Owner'
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def is_owner(self, user):
        """Check if the given user is the owner of this product."""
        return self.user == user

    def get_discounted_price(self):
        """Calculate the discounted price if a valid discount exists."""
        if self.has_valid_discount():
            discount_amount = (self.price * self.discount_percent) / 100
            return self.price - discount_amount
        return self.price

    def has_valid_discount(self):
        """Check if the product has a valid discount."""
        now = timezone.now()
        has_discount = self.discount_percent > 0
        
        if not has_discount:
            return False
            
        if self.discount_start_date and self.discount_end_date:
            return has_discount and self.discount_start_date <= now <= self.discount_end_date
        elif self.discount_start_date:
            return has_discount and self.discount_start_date <= now
        elif self.discount_end_date:
            return has_discount and now <= self.discount_end_date
        
        return has_discount

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percent = models.IntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_discount_amount(self):
        if self.discount_percent > 0:
            return (self.original_price - self.price) * self.quantity
        return 0

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    discount_percent_at_time = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # Store the current price and discount when adding to cart
        if not self.price_at_time:
            self.price_at_time = self.product.price
            if self.product.has_valid_discount():
                self.discount_percent_at_time = self.product.discount_percent
        super().save(*args, **kwargs)

    def get_price(self):
        """Get the effective price (with discount if applicable)"""
        if self.discount_percent_at_time > 0:
            discount_amount = (self.price_at_time * self.discount_percent_at_time) / 100
            return self.price_at_time - discount_amount
        return self.price_at_time

    def get_cost(self):
        """Calculate total cost for this item"""
        return self.get_price() * self.quantity

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news/%Y/%m/%d/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=[('draft', 'Draft'), ('published', 'Published')], default='draft')

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'news'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('store:news_detail', args=[self.slug])
