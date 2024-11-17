
from apps.home.models import UserTourStep

def get_user_tour_step(user_tour, step_name):
    return UserTourStep.objects.get(step_name=step_name, tour=user_tour)

def get_user_tour_steps(user_tour):
    return UserTourStep.objects.filter(tour=user_tour)