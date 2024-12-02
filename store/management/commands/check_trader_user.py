from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Check details of testtrader user'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.get(username='testtrader')
            
            # Check user groups
            groups = user.groups.all()
            self.stdout.write(self.style.SUCCESS(f'User groups: {", ".join([g.name for g in groups])}'))
            
            # Check if user is in Trader group
            is_trader = user.groups.filter(name='Trader').exists()
            self.stdout.write(self.style.SUCCESS(f'Is in Trader group: {is_trader}'))
            
            # Additional user details
            self.stdout.write(self.style.SUCCESS(f'User ID: {user.id}'))
            self.stdout.write(self.style.SUCCESS(f'Email: {user.email}'))
            self.stdout.write(self.style.SUCCESS(f'Is Active: {user.is_active}'))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User testtrader does not exist!'))
