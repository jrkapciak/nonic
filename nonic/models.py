from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from nonic.storages import PublicMediaStorage


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Manufacturer(TimestampedModel):
    name = models.CharField(_("Name"), max_length=255, blank=False)

    def __str__(self):
        return self.name


class Style(TimestampedModel):
    name = models.CharField(_("Name"), max_length=255, blank=False, unique=True)

    def __str__(self):
        return self.name


class BeerSource(TimestampedModel):
    url = models.URLField(_("URL"), unique=True)
    beer = models.ForeignKey("nonic.Beer", verbose_name=_("Beer"), related_name="sources", on_delete=models.CASCADE)


class Beer(TimestampedModel):
    name = models.CharField(_("Name"), max_length=255, blank=False)
    code = models.CharField(_("Code"), max_length=255, blank=False, unique=True)
    description = models.TextField(_("Description"), blank=False)
    manufactured_by = models.ForeignKey(
        "nonic.Manufacturer", verbose_name=_("Manufacturer"), related_name="beers", on_delete=models.CASCADE
    )
    style = models.ManyToManyField("nonic.Style", verbose_name=_("Style"), related_name="beers", blank=True)
    volume = models.PositiveSmallIntegerField(_("Volume (ml)"), blank=True, default=500)
    alcohol = models.FloatField(_("Alcohol  %"), blank=True, null=True)
    extract = models.FloatField(_("Extract"), blank=True, null=True)
    tags = models.JSONField(_("Tags"), blank=True, default=dict)
    thumbnail = models.ImageField(_("thumbnail"), storage=PublicMediaStorage(), blank=True, null=True)
    country = models.CharField(_("Country"), max_length=255, blank=False)
    rating = models.PositiveSmallIntegerField(
        _("Rating"), blank=True, default=1, validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    rating_count = models.IntegerField(_("Rating count"), blank=True, default=0)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
