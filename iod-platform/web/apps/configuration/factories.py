# import factory
# from django.contrib.auth.models import User
# from django.utils import timezone
# from .models import AssetType
# from apps.home.models import Networth

# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = User

#     username = factory.Sequence(lambda n: f'user{n}')
#     email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
#     password = factory.PostGenerationMethodCall('set_password', 'password')
#     is_active = True
#     is_superuser = False
#     is_staff = False

# class NetworthFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Networth
#     name = factory.Faker('word')
#     amount = factory.Faker('pyint', min_value=100, max_value=100000)
#     user = factory.SubFactory(UserFactory)


# class AssetTypeFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = AssetType
#     name = factory.Sequence(lambda n: f'asset_type_{n}')
#     weightage = factory.Faker('pyint', min_value=1, max_value=10)
#     networth = factory.SubFactory(NetworthFactory) 
