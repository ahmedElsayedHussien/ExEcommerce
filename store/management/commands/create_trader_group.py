from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from store.models import Product

class Command(BaseCommand):
    help = 'Create Trader group with specific permissions'

    def handle(self, *args, **kwargs):
        # Get or create the Trader group
        trader_group, created = Group.objects.get_or_create(name='Trader')
        
        if created:
            self.stdout.write(self.style.SUCCESS('Trader group created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Trader group already exists'))
        
        # Get content type for Product model
        product_content_type = ContentType.objects.get_for_model(Product)
        
        # Define permissions
        permissions = [
            Permission.objects.get_or_create(
                codename='add_product',
                name='Can add product',
                content_type=product_content_type
            )[0],
            Permission.objects.get_or_create(
                codename='change_product',
                name='Can change product',
                content_type=product_content_type
            )[0],
            Permission.objects.get_or_create(
                codename='delete_product',
                name='Can delete product',
                content_type=product_content_type
            )[0],
        ]
        
        # Add permissions to the group
        trader_group.permissions.set(permissions)
        trader_group.save()
        
        self.stdout.write(self.style.SUCCESS('Added product-related permissions to Trader group'))
        
        # List all permissions in the group
        group_permissions = trader_group.permissions.all()
        self.stdout.write('Trader Group Permissions:')
        for perm in group_permissions:
            self.stdout.write(f'- {perm.name}')
