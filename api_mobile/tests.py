from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from users.tests.factories import UserFactory
from nonic.tests.factories import BeerFactory, BeerStyleFactory
from nonic.models import Beer

faker = Faker()


class BeerViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.user = UserFactory()

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.beer_list = cls.generate_list_of_beers()

    @classmethod
    def create_list_of_beer_styles(cls, number_of_styles=None):
        if not number_of_styles:
            number_of_styles = faker.pyint(min_value=1, max_value=99)
        return [BeerStyleFactory() for s in range(number_of_styles)]

    @classmethod
    def generate_list_of_beers(cls):
        beer_list = []
        number_of_beers = faker.pyint(min_value=1, max_value=999)
        beer_style_list = cls.create_list_of_beer_styles()
        for beer in range(number_of_beers):
            beer_list.append(
                BeerFactory.create(
                    style=faker.random_choices(elements=beer_style_list, length=faker.pyint(max_value=10))
                )
            )
        return beer_list

    def test_list_status_code(self):
        response = self.client.get(reverse("api-mobile:beers-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_all_element_count(self):
        response = self.client.get(reverse("api-mobile:beers-list"))
        self.assertEqual(response.data.get("count"), len(self.beer_list))

    def test_list_filter(self):
        beer_list_countries = [beer.country for beer in self.beer_list]
        most_popular_country = max(set(beer_list_countries), key=beer_list_countries.count)
        url = f'{reverse("api-mobile:beers-list")}?country={most_popular_country}'
        response = self.client.get(url)
        self.assertEqual(response.data.get("count"), beer_list_countries.count(most_popular_country))

    def test_add_new_beer_unauthorised(self):
        response = self.client.post(reverse("api-mobile:beers-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_beer_unauthorised(self):
        response = self.client.delete(reverse("api-mobile:beers-detail", kwargs={"code": self.beer_list[0].code}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_new_beer(self):
        self.client.force_authenticate(self.user)
        beer_data = {
            "code": faker.pyint(),
            "name": faker.company(),
            "description": faker.paragraph(variable_nb_sentences=False),
        }
        response = self.client.post(reverse("api-mobile:beers-list"), data=beer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("code"), str(beer_data["code"]))
