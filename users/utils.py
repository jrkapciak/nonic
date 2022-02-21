import datetime

from django.utils import timezone

from faker import Faker
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()
faker = Faker()


def get_tokens_for_user(user: User) -> dict[str:str]:
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def generate_otp(user: User) -> int:
    otp = faker.pyint(min_value=100000, max_value=999999)
    user.generated_otp = otp
    user.otp_exp_date = timezone.now() + datetime.timedelta(minutes=15)
    user.save(update_fields=["generated_otp", "otp_timestamp"])
    return user.generated_otp


def validate_otp(user: User, otp: int) -> bool:
    if not user.otp_exp_date or timezone.now() > user.otp_exp_date:
        return False
    if not otp == user.generated_otp:
        return False
    return True
