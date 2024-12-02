from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from store.models import Product, Category

class Command(BaseCommand):
    help = 'Create a test trader user with some products'

    def handle(self, *args, **kwargs):
        # Get or create Trader group
        trader_group, _ = Group.objects.get_or_create(name='Trader')
        
        # Create a test user
        username = 'testtrader'
        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            # Reset password
            user.set_password('testpassword123')
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email='testtrader@example.com',
                password='testpassword123'
            )
            user.groups.add(trader_group)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user {username}'))
        
        # Create a category if it doesn't exist
        category, _ = Category.objects.get_or_create(
            name='Test Category', 
            slug='test-category'
        )
        
        # Create some test products for this user
        product_data = [
            {
                'name': 'Classic T-Shirt',
                'slug': 'classic-t-shirt',
                'description': 'A comfortable classic t-shirt',
                'price': 19.99,
                'category': category,
                'available': True,
                'user': user
            },
            {
                'name': 'Vintage Hoodie',
                'slug': 'vintage-hoodie',
                'description': 'A warm vintage style hoodie',
                'price': 49.99,
                'category': category,
                'available': True,
                'user': user
            }
        ]
        
        # Create products, skipping if they already exist
        for data in product_data:
            try:
                Product.objects.get(slug=data['slug'])
                self.stdout.write(self.style.WARNING(f"Product {data['name']} already exists"))
            except Product.DoesNotExist:
                Product.objects.create(**data)
                self.stdout.write(self.style.SUCCESS(f"Created product {data['name']}"))
