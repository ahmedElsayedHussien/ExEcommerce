from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product, Cart, CartItem, Order, OrderItem, News
from .payment import create_payment_session
import json
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm, ProductForm, AuthenticationForm, NewsForm
from django.contrib.auth import login
from .decorators import trader_required
import logging
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 20)  # Show 20 products per page
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'store/product/list.html',
                 {'category': category,
                  'categories': categories,
                  'products': products})

def product_detail(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug, available=True)
        return render(request, 'store/product/detail.html', {'product': product})
    except Http404:
        messages.error(request, 'The product you are looking for does not exist.')
        return redirect('store:product_list')

@login_required
def cart_add(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        messages.success(request, f'{product.name} added to cart.')
        return redirect('store:cart_detail')
    return redirect('store:product_list')

@login_required
def cart_remove(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            
            messages.success(request, f'{product.name} removed from cart.')
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            messages.error(request, 'Item not found in cart.')
    
    return redirect('store:cart_detail')

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    return render(request, 'store/cart/detail.html',
                 {'cart': cart, 'cart_items': cart_items})

@login_required
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            city=request.POST['city'],
            postal_code=request.POST['postal_code'],
            mobile_number=request.POST.get('mobile_number', '')
        )
        
        for cart_item in cart.items.all():
            current_price = cart_item.get_price()  # Get the discounted price if applicable
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=current_price,
                original_price=cart_item.price_at_time,
                discount_percent=cart_item.discount_percent_at_time,
                quantity=cart_item.quantity
            )
        
        # Clear the cart
        cart.delete()
        
        # Redirect for payment
        return redirect('store:payment_process', order_id=order.id)
    
    return render(request, 'store/order/create.html',
                 {'cart': cart})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order/detail.html',
                 {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order/list.html',
                 {'orders': orders})

@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order has been deleted successfully.')
        return redirect('store:order_list')
    return render(request, 'store/order/delete.html', {'order': order})

@login_required
def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        try:
            # Create Paymob payment session
            payment_url = create_payment_session(order, request)
            return redirect(payment_url)
        except Exception as e:
            messages.error(request, 'Error processing payment. Please try again.')
            return redirect('store:order_detail', order_id=order.id)
    
    return render(request, 'store/payment/process.html', {'order': order})

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Update order status
    order.paid = True
    order.save()
    # Clear the cart
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()
    messages.success(request, 'Payment successful! Your order has been processed.')
    return redirect('store:order_detail', order.id)

@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    messages.warning(request, 'Payment was cancelled. Please try again.')
    return redirect('store:order_detail', order.id)

@login_required
def add_product(request):
    # Comprehensive logging
    import logging
    from django.http import HttpResponse
    logger = logging.getLogger(__name__)
    
    logger.error(f"Add Product View Called")
    logger.error(f"User: {request.user}")
    logger.error(f"User Authenticated: {request.user.is_authenticated}")
    logger.error(f"User Groups: {list(request.user.groups.values_list('name', flat=True))}")
    logger.error(f"Request Method: {request.method}")
    
    # Debug: print all groups and categories
    print("User Groups:", list(request.user.groups.all()))
    print("Available Categories:", list(Category.objects.all()))
    
    # Temporary debug: return a simple response to check if view is reached
    # return HttpResponse("Add Product View Reached")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        # Log form data for debugging
        logger.error(f"POST Data: {request.POST}")
        logger.error(f"FILES Data: {request.FILES}")
        
        if form.is_valid():
            # Log form validation details
            logger.error("Form is valid")
            
            # Ensure the current user is set as the product owner
            product = form.save(commit=False)
            product.user = request.user
            
            try:
                product.save()
                messages.success(request, 'Product added successfully.')
                return redirect('store:user_products')
            except Exception as e:
                # Log any save errors
                logger.error(f"Product save error: {str(e)}")
                messages.error(request, f'Error saving product: {str(e)}')
        else:
            # Log form errors
            logger.error(f"Form Errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = ProductForm()
    
    # Ensure categories exist
    categories = Category.objects.all()
    if not categories.exists():
        messages.warning(request, 'No categories available. Please create a category first.')
    
    return render(request, 'store/product/add.html', {
        'form': form, 
        'categories': categories
    })

@login_required
@trader_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('store:product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product/edit.html', {'form': form, 'product': product})

@login_required
def user_products(request):
    # If admin is viewing another user's products
    target_user_id = request.GET.get('user')
    if request.user.is_staff and target_user_id:
        target_user = get_object_or_404(get_user_model(), id=target_user_id)
        products = Product.objects.filter(user=target_user)
        context = {
            'products': products,
            'target_user': target_user,
            'viewing_as_admin': True
        }
    else:
        # Regular user viewing their own products
        products = Product.objects.filter(user=request.user)
        context = {
            'products': products,
            'viewing_as_admin': False
        }
    
    paginator = Paginator(products, 10)  # Show 10 products per page
    page = request.GET.get('page', 1)
    
    try:
        products_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        products_page = paginator.page(1)
    
    context['products'] = products_page
    context['total_products'] = products.count()
    
    return render(request, 'store/product/user_products.html', context)

@login_required
@trader_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('store:product_list')
    return render(request, 'store/product/delete.html', {'product': product})

def news_list(request):
    news = News.objects.filter(status='published').order_by('-created')
    paginator = Paginator(news, 10)  # Show 10 news items per page
    page = request.GET.get('page')
    
    try:
        news_items = paginator.page(page)
    except PageNotAnInteger:
        news_items = paginator.page(1)
    except EmptyPage:
        news_items = paginator.page(paginator.num_pages)
    
    return render(request, 'store/news/list.html', {'news_items': news_items})

def news_detail(request, slug):
    news_item = get_object_or_404(News, slug=slug, status='published')
    return render(request, 'store/news/detail.html', {'news_item': news_item})

@csrf_exempt
def payment_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get the order ID from the merchant_order_id
        order_id = data.get('merchant_order_id')
        success = data.get('success')
        
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                if success:
                    order.paid = True
                    order.save()
                    # Clear the cart
                    cart = Cart.objects.get(user=order.user)
                    cart.items.all().delete()
                return JsonResponse({'status': 'success'})
            except Order.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Order not found'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_open_orders(request):
    open_orders = Order.objects.all().order_by('-created')
    return render(request, 'store/order/admin_open_orders.html', {
        'open_orders': open_orders
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Update order details
        order.first_name = request.POST.get('first_name')
        order.last_name = request.POST.get('last_name')
        order.email = request.POST.get('email')
        order.address = request.POST.get('address')
        order.city = request.POST.get('city')
        order.mobile_number = request.POST.get('mobile_number')
        
        # Update order items quantities
        for item in order.items.all():
            quantity_key = f'quantity_{item.id}'
            if quantity_key in request.POST:
                new_quantity = int(request.POST[quantity_key])
                if new_quantity > 0:
                    item.quantity = new_quantity
                    item.save()
        
        order.save()
        messages.success(request, 'Order updated successfully.')
        return redirect('store:admin_open_orders')
    
    return render(request, 'store/order/edit_order.html', {'order': order})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, 'Order deleted successfully.')
    return redirect('store:admin_open_orders')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_trader_list(request):
    trader_group = Group.objects.get(name='Trader')
    traders = get_user_model().objects.filter(groups=trader_group).order_by('-date_joined')
    return render(request, 'store/admin/trader_list.html', {
        'traders': traders
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_remove_trader(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    trader_group = Group.objects.get(name='Trader')
    
    if user.groups.filter(name='Trader').exists():
        user.groups.remove(trader_group)
        messages.success(request, f'Successfully removed trader status from {user.username}')
    else:
        messages.warning(request, f'{user.username} is not a trader')
    
    return redirect('store:admin_trader_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_item = form.save()
            messages.success(request, 'News article created successfully.')
            return redirect('store:news_detail', slug=news_item.slug)
    else:
        form = NewsForm()
    return render(request, 'store/news/form.html', {'form': form, 'title': 'Create News Article'})

@login_required
@user_passes_test(lambda u: u.is_staff)
def news_edit(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news_item)
        if form.is_valid():
            news_item = form.save()
            messages.success(request, 'News article updated successfully.')
            return redirect('store:news_detail', slug=news_item.slug)
    else:
        form = NewsForm(instance=news_item)
    return render(request, 'store/news/form.html', {'form': form, 'title': 'Edit News Article'})

@login_required
@user_passes_test(lambda u: u.is_staff)
def news_delete(request, slug):
    news_item = get_object_or_404(News, slug=slug)
    if request.method == 'POST':
        news_item.delete()
        messages.success(request, 'News article deleted successfully.')
        return redirect('store:news_list')
    return render(request, 'store/news/delete.html', {'news_item': news_item})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Check if there's a 'next' parameter
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Default to product list view
            return redirect('store:product_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:product_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
