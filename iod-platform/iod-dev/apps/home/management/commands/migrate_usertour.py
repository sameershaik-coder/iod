from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.home.models import UserTour, UserTourStep
from apps.home.actions import usertour
class Command(BaseCommand):
    help = 'Migrate existing users to UserTour and UserTourSteps'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            qs = UserTour.objects.filter(user=user)
            if(len(qs)==0):
                print("Checking tour exists for user...")
                print(str(user.email) + " : "+ str(len(qs)))
                usertour.do_create_user_tour_for_new_user(user=user)
                print("Created tour for user : "+ str(user.email))
                
            