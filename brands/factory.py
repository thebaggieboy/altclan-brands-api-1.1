from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory import Sequence, PostGenerationMethodCall, sequence

class BrandFactory(DjangoModelFactory):
    brand_name = Faker('company')
    brand_bio = Faker('sentence')
    slug = Faker('slug')
    date_created = Faker('date')
    username = Faker('user_name')
    brand_bio = Faker('sentence')
    
    class Meta:
        model = 'brands.Brand'
        
class MerchandiseFactory(DjangoModelFactory):
    merchandise_name = Faker('company')
    merchandise_color = Faker('color')
    #merchandise_size = Faker('size')
    slug = Faker('slug')

    class Meta:
        model = 'brands.Merchandise'



