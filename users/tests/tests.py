from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.tests.factories import UserFactory

faker = Faker()
User = get_user_model()


class UsersModelTests(TestCase):
    def test_create_user(self):
        email = faker.email()
        user = User.objects.create_user(username=faker.name(), email=email, password=faker.password())
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_more_than_one_user(self):
        User.objects.create_user(
            username=faker.name(), email=faker.email(), password=faker.password(), phone=faker.phone_number()
        )
        User.objects.create_user(
            username=faker.name(), email=faker.email(), password=faker.password(), phone=faker.phone_number()
        )
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_with_unique_email(self):
        email = faker.email()
        # first user
        user = User.objects.create_user(username=faker.name(), email=email, password=faker.password())
        self.assertEqual(user.email, email)

        # second user
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username=faker.name(), email=email, password=faker.password())

    def test_create_user_with_unique_phone(self):
        phone = faker.phone_number()
        # first user
        user = User.objects.create_user(
            username=faker.name(), email=faker.email(), phone=phone, password=faker.password()
        )
        self.assertEqual(phone, user.phone)

        # second user
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username=faker.name(), email=faker.email(), phone=phone, password=faker.password()
            )


class TestRegisterView(APITestCase):
    def test_register_response_contains_tokens(self):
        client = APIClient()
        data = {
            "password": faker.password(),
            "username": faker.first_name(),
            "phone": faker.phone_number(),
            "email": faker.email(),
        }
        response = client.post(reverse("users:register"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_was_created(self):
        client = APIClient()
        data = {
            "password": faker.password(),
            "username": faker.first_name(),
            "phone": faker.phone_number(),
            "email": faker.email(),
        }
        response = client.post(reverse("users:register"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(username=data["username"], email=data["email"], phone=data["phone"]).exists()
        )

    def test_register_username_is_taken(self):
        user = UserFactory()
        client = APIClient()
        data = {
            "password": faker.password(),
            "username": user.username,
            "email": faker.email(),
            "phone": faker.phone_number(),
        }
        response = client.post(reverse("users:register"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("username")[0], "A user with that username already exists.")
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
        self.assertEqual(User.objects.count(), 1)
