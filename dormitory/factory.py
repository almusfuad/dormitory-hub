import factory
from .models import Location, Dormitory
from factory.faker import Faker
from faker.providers import BaseProvider
import random

class CustomCountryProvider(BaseProvider):
      def custom_country_from_region(self, region):
            countries_by_region = {
                  "Europe": ["France", "Germany", "Netherlands", "Belgium", "Denmark", "Norway", "Finland", "Ireland", "Sweden", "Czech Republic"],
                  "Asia": ["China", "India", "Japan", "Korea"],
                  "North-America": ["USA", "Canada"]
            }
            
            countries = countries_by_region.get(region, [])
            if not countries:
                  raise ValueError(f"No countries found for the region '{region}'")
            return self.random_element(countries)


def register_custom_country_provider():
      factory.Faker.add_provider(CustomCountryProvider)

register_custom_country_provider()


      
class LocationFactory(factory.django.DjangoModelFactory):
      class Meta:
            model = Location
      
      location = factory.Faker("custom_country_from_region",
                               region = factory.LazyAttribute(
                                     lambda obj: random.choice(["Europe", "Asia", "North-America"])
                               )
                        )