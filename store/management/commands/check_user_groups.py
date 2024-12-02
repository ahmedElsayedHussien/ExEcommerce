from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Check user group memberships'

    def handle(self, *args, **kwargs):
        # Check testtrader user
        try:
            user = User.objects.get(username='testtrader')
            
            # Get user's groups
            groups = user.groups.all()
            
            if groups:
                self.stdout.write(self.style.SUCCESS('User Groups:'))
                for group in groups:
                    self.stdout.write(f'- {group.name}')
            else:
                self.stdout.write(self.style.WARNING('User is not in any groups'))
        
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User testtrader does not exist!'))
