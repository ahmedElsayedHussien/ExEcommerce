import os
import django
import random
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Category, Product

def add_more_products():
    # Sample product data
    electronics_products = [
        ("Gaming Laptop", "High-performance gaming laptop with RTX 3080", 1499.99),
        ("4K Monitor", "32-inch 4K HDR monitor", 499.99),
        ("Wireless Earbuds", "Noise-cancelling wireless earbuds", 149.99),
        ("Smart Watch", "Fitness tracking smart watch", 199.99),
        ("Tablet", "10-inch tablet with stylus support", 399.99),
        ("Keyboard", "Mechanical gaming keyboard", 89.99),
        ("Mouse", "Wireless gaming mouse", 59.99),
        ("Webcam", "1080p HD webcam", 79.99),
        ("Power Bank", "20000mAh power bank", 49.99),
        ("Speaker", "Bluetooth portable speaker", 129.99),
    ]

    clothing_products = [
        ("Denim Jacket", "Classic denim jacket", 79.99),
        ("Leather Boots", "Genuine leather boots", 149.99),
        ("Wool Sweater", "Warm wool sweater", 89.99),
        ("Cotton T-Shirt", "Premium cotton t-shirt", 29.99),
        ("Jeans", "Slim fit jeans", 69.99),
        ("Hoodie", "Comfortable hoodie", 59.99),
        ("Sneakers", "Athletic sneakers", 99.99),
        ("Dress Shirt", "Formal dress shirt", 49.99),
        ("Winter Coat", "Warm winter coat", 199.99),
        ("Sports Shorts", "Athletic shorts", 34.99),
    ]

    books_products = [
        ("Python Programming", "Learn Python programming", 39.99),
        ("Web Development", "Full-stack web development guide", 49.99),
        ("Data Science", "Introduction to data science", 44.99),
        ("AI and ML", "Artificial Intelligence and Machine Learning", 54.99),
        ("JavaScript Guide", "Modern JavaScript programming", 39.99),
        ("Django Framework", "Django web development", 44.99),
        ("Database Design", "Database design principles", 49.99),
        ("Cloud Computing", "Introduction to cloud computing", 54.99),
        ("Cybersecurity", "Cybersecurity fundamentals", 49.99),
        ("Software Architecture", "Software architecture patterns", 59.99),
    ]

    try:
        # Get categories
        electronics = Category.objects.get(name='Electronics')
        clothing = Category.objects.get(name='Clothing')
        books = Category.objects.get(name='Books')

        # Add electronics products
        for name, description, price in electronics_products:
            product_name = f"{name} {random.randint(1000, 9999)}"
            Product.objects.create(
                category=electronics,
                name=product_name,
                slug=slugify(product_name),  # Generate slug from name
                description=description,
                price=price,
                available=True
            )

        # Add clothing products
        for name, description, price in clothing_products:
            product_name = f"{name} {random.randint(1000, 9999)}"
            Product.objects.create(
                category=clothing,
                name=product_name,
                slug=slugify(product_name),  # Generate slug from name
                description=description,
                price=price,
                available=True
            )

        # Add books products
        for name, description, price in books_products:
            product_name = f"{name} {random.randint(1000, 9999)}"
            Product.objects.create(
                category=books,
                name=product_name,
                slug=slugify(product_name),  # Generate slug from name
                description=description,
                price=price,
                available=True
            )

        print("Successfully added 30 more products with slugs!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    add_more_products()
