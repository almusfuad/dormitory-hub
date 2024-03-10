import factory
from .models import Location, Dormitory
from factory.faker import Faker
from factory.django import DjangoModelFactory
# from faker.providers import BaseProvider
import random

      
class LocationFactory(DjangoModelFactory):
      class Meta:
            model = Location
      
      @classmethod
      def _generate_unique_location(cls, region):
            countries_by_region = {
                  "Europe": ["France", "Germany", "Netherlands", "Belgium", "Denmark", "Norway", "Finland", "Ireland", "Sweden", "Czech Republic"],
                  "Asia": ["China", "India", "Japan", "Korea"],
                  "North-America": ["USA", "Canada"]
            }
            countries = countries_by_region.get(region, [])
            new_location = random.choice(countries)
            while Location.objects.filter(location = new_location).exists():
                  new_location = random.choice(countries)
            return new_location
      
      
      location = factory.LazyAttribute(lambda obj: LocationFactory._generate_unique_location(random.choice(["Europe", "Asia", "North-America"])))
      

class DormitoryFactory(DjangoModelFactory):
      class Meta:
            model = Dormitory
            
      name = factory.Faker('company')
      address = factory.Faker('address')
      image = factory.Faker('image_url', width = 800, height = 600)
      dormitory_type = factory.Faker('random_element', elements = ['girls', 'boys'])
      facilities = factory.Faker('random_element', elements = ['super', 'regular'])
      cost_per_night = factory.Faker('random_number', digits = 2)
      cost_per_month = factory.Faker('random_number', digits = 3)
      available_seats = factory.Faker('random_number', digits = 2)
      
      @factory.lazy_attribute
      def location(self):
            return Location.objects.order_by('?').first()