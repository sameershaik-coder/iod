# import factory
# from django.contrib.auth.models import User
# from django.utils import timezone
# from apps.home.models import(BaseUnit,Networth)

# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = User

#     username = factory.Sequence(lambda n: f'user{n}')
#     email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
#     password = factory.PostGenerationMethodCall('set_password', 'password')
#     is_active = factory.Faker('pybool')
#     is_superuser = factory.Faker('pybool')

# class NetworthFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Networth
#     name = factory.Faker('word')
#     amount = factory.Faker('pyint', min_value=100, max_value=100000)
#     user = factory.SubFactory(UserFactory)

# class BaseUnitFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = BaseUnit
#     name = factory.Sequence(lambda n: f'baseunit_type_{n}')
#     value = factory.Faker('pyint', min_value=100000, max_value=100000)
#     networth = factory.SubFactory(NetworthFactory) 

