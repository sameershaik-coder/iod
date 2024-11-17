from apps.home.models import UserTour, UserTourStep
from django.contrib.auth.models import User
from typing import Optional
from django.db import transaction

def get_user_tour(user):
    return UserTour.objects.get(user=user)

def do_create_user_tour_for_new_user(
    user: User
) -> UserTour:
    with transaction.atomic():
        user_tour = UserTour.objects.create(
            user=user,
            status="Not-Started"
        )
        for i in range(9):
            step_name = str(str(i+1))
            UserTourStep.objects.create(
                step_name=step_name,
                status="Not-Started",
                tour=user_tour
            )
    return user_tour
 
def do_update_user_tour_for_new_user(user : User):
    user_tour = UserTour.objects.get(user=user)
    user_tour_steps = UserTourStep.objects.filter(tour = user_tour)
    steps_completed_count = 0
    for user_tour_step in user_tour_steps:
        if user_tour_step.status == "Completed":
            steps_completed_count = steps_completed_count + 1
    if steps_completed_count == 0:
        user_tour_status = "Not-Started"
    elif steps_completed_count == 9 :
        user_tour_status = "Completed"
    elif steps_completed_count > 0 and steps_completed_count < 9:
        user_tour_status = "In-Progress"
    user_tour.status = user_tour_status
    user_tour.save()

    