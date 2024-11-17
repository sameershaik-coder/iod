# Import the base command class and the User model
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

# Define the command class
class Command (BaseCommand):
    # Add a help text for the command
    help = 'Delete a user by email'

    # Define the arguments that the command expects
    def add_arguments (self, parser):
        # Add a required positional argument for the email
        parser.add_argument ('email', type=str, help='The email of the user to delete')

    # Define the logic of the command
    def handle (self, *args, **options):
        # Get the email from the options
        email = options['email']

        # Try to get the user by email and delete it
        try:
            user = User.objects.get (email=email)
            user.delete ()
            # Print a success message
            self.stdout.write (self.style.SUCCESS (f'Deleted user {email}'))
        except User.DoesNotExist:
            # Print an error message
            self.stderr.write (self.style.ERROR (f'User {email} does not exist'))
