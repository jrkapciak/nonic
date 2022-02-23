import datetime
import boto3
import os

from django.utils import timezone
from django.utils.translation import gettext as _

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
    user.otp = faker.pyint(min_value=100000, max_value=999999)
    user.otp_exp_date = timezone.now() + datetime.timedelta(minutes=15)
    user.save(update_fields=["otp", "otp_exp_date"])
    return user.otp


def validate_otp(user: User, otp: int) -> bool:
    if user.otp_limit_reached:
        return False
    if not user.otp_exp_date or timezone.now() > user.otp_exp_date:
        invalid_otp(user)
        return False
    if not otp == user.otp:
        invalid_otp(user)
        return False
    return True


def send_otp(user: User) -> bool:
    if not os.environ.get("OTP_ENABLED"):
        return False

    otp_text = _(f"This is your One Time Password {user.otp}")
    client = boto3.client(
        "sns",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
        region_name=os.environ.get("AWS_SNS_REGION"),
    )
    client.publish(PhoneNumber=user.phone, Message=otp_text)
    return True


def invalid_otp(user) -> None:
    user.invalid_otp_entered += 1
    user.save(update_fields=["invalid_otp_entered"])
    send_otp(user)
