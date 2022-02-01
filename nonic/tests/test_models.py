from django.test import TestCase

from users.tests.factories import UserFactory
from nonic.tests.factories import BeerFactory
from faker import Faker
from nonic.models import BeerRating

faker = Faker()


class BeerRatingModelTest(TestCase):
    def test_rating(self):
        user_1 = UserFactory()
        user_2 = UserFactory()

        beer = BeerFactory.create()

        user_1_rating = faker.pyint(min_value=1, max_value=5)
        user_2_rating = faker.pyint(min_value=1, max_value=5)

        BeerRating.objects.create(user=user_1, beer=beer, rating=user_1_rating)
        BeerRating.objects.create(user=user_2, beer=beer, rating=user_2_rating)

        beer.refresh_from_db()

        self.assertEqual(beer.rating, (user_1_rating + user_2_rating) / 2)
