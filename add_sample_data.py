import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Category, Product

def add_sample_data():
    # Create categories
    categories = [
        {'name': 'Electronics', 'slug': 'electronics'},
        {'name': 'Clothing', 'slug': 'clothing'},
        {'name': 'Books', 'slug': 'books'},
    ]

    for cat_data in categories:
        Category.objects.get_or_create(
            name=cat_data['name'],
            slug=cat_data['slug']
        )

    # Create products
    products = [
        {
            'category': 'electronics',
            'name': 'Smartphone X',
            'slug': 'smartphone-x',
            'description': 'Latest smartphone with amazing features',
            'price': 699.99
        },
        {
            'category': 'electronics',
            'name': 'Laptop Pro',
            'slug': 'laptop-pro',
            'description': 'Powerful laptop for professionals',
            'price': 1299.99
        },
        {
            'category': 'clothing',
            'name': 'Classic T-Shirt',
            'slug': 'classic-t-shirt',
            'description': 'Comfortable cotton t-shirt',
            'price': 19.99
        },
        {
            'category': 'clothing',
            'name': 'Denim Jeans',
            'slug': 'denim-jeans',
            'description': 'High-quality denim jeans',
            'price': 49.99
        },
        {
            'category': 'books',
            'name': 'Python Programming',
            'slug': 'python-programming',
            'description': 'Learn Python programming from scratch',
            'price': 29.99
        },
        {
            'category': 'books',
            'name': 'Web Development Guide',
            'slug': 'web-development-guide',
            'description': 'Complete guide to modern web development',
            'price': 34.99
        },
    ]

    for prod_data in products:
        category = Category.objects.get(slug=prod_data['category'])
        Product.objects.get_or_create(
            category=category,
            name=prod_data['name'],
            slug=prod_data['slug'],
            description=prod_data['description'],
            price=prod_data['price']
        )

    print("Sample data added successfully!")

if __name__ == '__main__':
    add_sample_data()
