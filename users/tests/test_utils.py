from datetime import timedelta
from unittest.mock import patch

from django.utils import timezone
from faker import Faker

from users.tests.factories import UserFactory
from users.utils import generate_otp, validate_otp
from django.test import TestCase

faker = Faker()


class UtilsTestCaste(TestCase):
    @patch("django.utils.timezone.now")
    def test_generated_otp_timestamp(self, mock_timezone_now):
        mock_timezone_now.return_value = faker.date_time()
        user = UserFactory()
        generate_otp(user)
        otp_exp_date = timezone.now() + timedelta(minutes=15)
        self.assertEqual(user.otp_exp_date, otp_exp_date)

    def test_generated_otp_code(self):
        user = UserFactory()
        otp = generate_otp(user)

        self.assertIsInstance(otp, int)
        self.assertIsInstance(user.otp, int)
        self.assertEqual(otp, user.otp)

    def test_invalidate_otp(self):
        user = UserFactory()
        generate_otp(user)
        invalid_otp = faker.pyint(min_value=100000, max_value=999999)
        self.assertFalse(validate_otp(user, invalid_otp))

    def test_invalidate_otp_limit_reached(self):
        user = UserFactory()
        generate_otp(user)

        for i in range(faker.pyint(min_value=3, max_value=10)):
            invalid_otp = faker.pyint(min_value=100000, max_value=999999)
            validate_otp(user, invalid_otp)
            if i < 2:
                self.assertFalse(user.otp_limit_reached)
                continue
            self.assertTrue(user.otp_limit_reached)

    def test_validate_otp(self):
        user = UserFactory()
        otp = generate_otp(user)
        self.assertTrue(validate_otp(user, otp))

    @patch("django.utils.timezone.now")
    def test_generated_otp_exp(self, mock_timezone_now):
        user = UserFactory()
        mock_timezone_now.return_value = faker.date_time()
        generate_otp(user)
        mock_timezone_now.return_value = mock_timezone_now.return_value + timedelta(
            minutes=faker.pyint(min_value=16, max_value=999)
        )
        invalid_otp = faker.pyint(min_value=100000, max_value=999999)
        self.assertFalse(validate_otp(user, invalid_otp))
        self.assertTrue(user.otp_exp_date < timezone.now())

    def test_validate_otp_no_otp_generated(self):
        user = UserFactory()
        invalid_otp = faker.pyint(min_value=100000, max_value=999999)
        self.assertFalse(validate_otp(user, invalid_otp))
