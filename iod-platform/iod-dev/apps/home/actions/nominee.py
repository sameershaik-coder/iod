from apps.home.models import UserNominee, UserProfile
from django.contrib.auth.models import User
from typing import Optional
from apps.home.actions import(
    networth as networth_actions,
    userprofile as userprofile_actions,
    usertour as usertour_actions
)
from django.db import transaction

def update_model_fields(instance: UserNominee, update_data):
    # Iterate through the dictionary of update data
    for field, value in update_data.items():
        # Update the model instance's field with the provided value using setattr
        setattr(instance, field, value)
    
    # Save the instance to commit the changes to the database
    instance.save()
    
    # Return the updated instance
    return instance

def get_nominee_or_None(user: User) -> Optional[UserNominee]:
    nominee_qs = get_nominee_qs(user)
    if(len(nominee_qs)==1):
        return nominee_qs[0]
    else:
        return None    

def get_nominee_qs(user: User) -> Optional[UserNominee]:
    nominee_qs = UserNominee.objects.filter(user=user)
    return nominee_qs
    

def do_create_nominee(
    name: str,
    email: str,
    user: User,
) -> UserNominee:
    with transaction.atomic():
        user_nominee = UserNominee.objects.create(
            name = name,
            email = email,
            status = "A",
            user=user
        )
    return user_nominee