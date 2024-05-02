from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory import Sequence, PostGenerationMethodCall, sequence

class UserFactory(DjangoModelFactory):
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'secret')

    #username = 
    class Meta:
        model = 'account.CustomUser'
        #django_get_or_create('email')


