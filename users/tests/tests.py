from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from faker import Faker

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
        User.objects.create_user(username=faker.name(), email=faker.email(), password=faker.password())
        User.objects.create_user(username=faker.name(), email=faker.email(), password=faker.password())
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_with_unique_email(self):
        email = faker.email()
        # first user
        user = User.objects.create_user(username=faker.name(), email=email, password=faker.password())
        self.assertEqual(user.email, email)

        # second user
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username=faker.name(), email=email, password=faker.password())
