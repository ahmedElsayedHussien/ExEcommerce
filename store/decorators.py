from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Product

def trader_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated and in the trader group
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        # Check if user is in the trader group (case-insensitive)
        if not request.user.groups.filter(name__iexact='Trader').exists():
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('store:product_list')
        
        # If the view takes a product_id, check ownership
        if 'product_id' in kwargs:
            product = get_object_or_404(Product, id=kwargs['product_id'])
            if not product.is_owner(request.user):
                messages.error(request, 'You can only modify your own products.')
                return redirect('store:product_list')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
