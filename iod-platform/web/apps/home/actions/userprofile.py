from apps.home.models import UserProfile
from django.contrib.auth.models import User
from typing import Optional

def update_model_fields(instance: UserProfile, update_data):
    # Iterate through the dictionary of update data
    for field, value in update_data.items():
        # Update the model instance's field with the provided value using setattr
        setattr(instance, field, value)
    
    # Save the instance to commit the changes to the database
    instance.save()
    
    # Return the updated instance
    return instance

def get_user_profile(user: User) -> Optional[UserProfile]:
    return UserProfile.objects.get(user=user)

def do_create_user_profile(
    user: User,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    address: Optional[str] = None,
    bio: Optional[str] = None,
    country: Optional[str] = None,
) -> UserProfile:
    user_profile = UserProfile.objects.create(
        first_name=first_name,
        last_name=last_name,
        address=address,
        bio=bio,
        user=user,
        country=country,
        subscription_type = "F"
    )
    return user_profile
