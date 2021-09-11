from django.db import models
from django.utils.translation import ugettext_lazy as _

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


class Beer(TimestampedModel):
    name = models.CharField(_("Name"), max_length=255, blank=False)
    code = models.CharField(_("Code"), max_length=255, blank=False)
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

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name
