from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.test import Client

class Command(BaseCommand):
    help = 'Test login functionality'

    def handle(self, *args, **kwargs):
        # Create a test client
        client = Client()

        # Attempt to log in
        username = 'testtrader'
        password = 'testpassword123'

        # First, verify the user exists
        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.SUCCESS(f'User {username} found'))
            self.stdout.write(self.style.SUCCESS(f'User groups: {", ".join([g.name for g in user.groups.all()])}'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
            return

        # Attempt authentication
        user = authenticate(username=username, password=password)
        if user is not None:
            self.stdout.write(self.style.SUCCESS('Authentication successful'))
            
            # Attempt to log in via client
            login_response = client.login(username=username, password=password)
            if login_response:
                self.stdout.write(self.style.SUCCESS('Client login successful'))
            else:
                self.stdout.write(self.style.ERROR('Client login failed'))
        else:
            self.stdout.write(self.style.ERROR('Authentication failed'))
