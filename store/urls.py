from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='category_list'),
    path('user/products/', views.user_products, name='user_products'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/', views.cart_detail, name='cart_detail'),
    
    # Admin order management
    path('orders/open/all/', views.admin_open_orders, name='admin_open_orders'),
    path('orders/<int:order_id>/edit/', views.admin_edit_order, name='admin_edit_order'),
    path('orders/<int:order_id>/delete/', views.admin_delete_order, name='admin_delete_order'),
    
    # Admin trader management
    path('traders/all/', views.admin_trader_list, name='admin_trader_list'),
    path('traders/remove/<int:user_id>/', views.admin_remove_trader, name='admin_remove_trader'),
    
    # Regular order URLs
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/create/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/delete/', views.order_delete, name='order_delete'),
    
    # Payment URLs
    path('payment/<int:order_id>/process/', views.payment_process, name='payment_process'),
    path('payment/<int:order_id>/success/', views.payment_success, name='payment_success'),
    path('payment/<int:order_id>/cancel/', views.payment_cancel, name='payment_cancel'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    
    # News URLs
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/<slug:slug>/edit/', views.news_edit, name='news_edit'),
    path('news/<slug:slug>/delete/', views.news_delete, name='news_delete'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    
    # Product management URLs - specific URLs first
    path('product/add/', views.add_product, name='add_product'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    # Generic product URL last
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
