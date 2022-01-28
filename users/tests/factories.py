from factory.django import DjangoModelFactory
from faker import Faker

from users import models

faker = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ("email", "username")

    email = faker.email
    username = faker.first_name
