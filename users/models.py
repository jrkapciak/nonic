from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    otp = models.PositiveIntegerField(_("otp"), blank=True, null=True)
    otp_exp_date = models.DateTimeField(_("otp valid to"), blank=True, null=True)
    invalid_otp_entered = models.PositiveSmallIntegerField(
        _("invalid otp entered"),
        validators=[MaxValueValidator(3), MinValueValidator(0)],
        default=0,
        blank=True,
        null=True,
    )
    phone = models.CharField(_("phone"), max_length=64, blank=False, unique=True)

    @property
    def otp_limit_reached(self):
        return self.invalid_otp_entered > 2
