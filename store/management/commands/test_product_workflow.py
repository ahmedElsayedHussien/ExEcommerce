from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Product, Category
from django.core.files.uploadedfile import SimpleUploadedFile

class Command(BaseCommand):
    help = 'Test full product management workflow'

    def handle(self, *args, **kwargs):
        # Get the test trader user
        try:
            user = User.objects.get(username='testtrader')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Test trader user not found!'))
            return

        # Get or create a test category
        category, _ = Category.objects.get_or_create(
            name='Test Category', 
            slug='test-category'
        )

        # Create a test image
        test_image = SimpleUploadedFile(
            name='test_product.jpg', 
            content=b'test image content',
            content_type='image/jpeg'
        )

        # Test product creation
        try:
            new_product = Product.objects.create(
                name='Test Workflow Product',
                slug='test-workflow-product',
                description='A product created during workflow testing',
                price=29.99,
                category=category,
                user=user,
                image=test_image,
                available=True
            )
            self.stdout.write(self.style.SUCCESS(f'Created test product: {new_product.name}'))

            # Verify product ownership
            if new_product.user != user:
                self.stdout.write(self.style.ERROR('Product user assignment failed!'))
            
            # Check if product is in user's products
            user_products = Product.objects.filter(user=user)
            if new_product not in user_products:
                self.stdout.write(self.style.ERROR('Product not found in user\'s products!'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Product found in user\'s products. Total: {user_products.count()}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Product creation failed: {str(e)}'))
