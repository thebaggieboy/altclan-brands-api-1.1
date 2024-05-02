import random
from django.db import transaction
from django.core.management.base import BaseCommand
from account.factory import UserFactory
from brands.factory import BrandFactory, MerchandiseFactory
from halo import Halo

class Command(BaseCommand):
    help = "Generate fake data and seed their models with them"

    def _generate_users(self, amount:int):
        for _ in range(amount):
            UserFactory()

    def _generate_brand(self, amount:int):
        for _ in range(amount):
            BrandFactory()

    def _generate_merchandise(self, amount:int):
        for _ in range(amount):
            MerchandiseFactory()

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='The amount of fake data')

    @Halo(text='Generating data ....', spinner='dots', color='blue', text_color='blue')
    def handle(self, *args, **options):
        amount = options.get('amount', 10)
        #print(amount)
        #self._generate_users(amount)
        self._generate_brand(amount)
        #self._generate_merchandise(amount)

