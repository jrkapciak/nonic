from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg
from nonic.storages import PublicMediaStorage

User = get_user_model()


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
        "nonic.Manufacturer",
        verbose_name=_("Manufacturer"),
        related_name="beers",
        on_delete=models.CASCADE,
        null=True,
    )
    style = models.ManyToManyField("nonic.Style", verbose_name=_("Style"), related_name="beers", blank=True)
    volume = models.PositiveSmallIntegerField(_("Volume (ml)"), blank=True, default=500)
    alcohol = models.FloatField(_("Alcohol  %"), blank=True, null=True)
    extract = models.FloatField(_("Extract"), blank=True, null=True)
    tags = models.JSONField(_("Tags"), blank=True, default=dict)
    thumbnail = models.ImageField(_("thumbnail"), storage=PublicMediaStorage(), blank=True, null=True)
    country = models.CharField(_("Country"), max_length=255, blank=True)
    rating = models.DecimalField(
        _("Rating"),
        blank=True,
        default=1,
        max_digits=3,
        decimal_places=2,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
    )
    rating_count = models.IntegerField(_("Rating count"), blank=True, default=0)
    favorites_count = models.IntegerField(_("Favorite count"), blank=True, default=0)
    favorites = models.ManyToManyField(User, through="UserFavorite", related_name="favorite_beer", blank=True)
    users_rating = models.ManyToManyField(User, through="BeerRating", related_name="beer_rating", blank=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class BeerTemplate(Beer):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    draft_created = models.DateTimeField(auto_now_add=True)
    draft_updated = models.DateTimeField(auto_now=True)


class BeerRating(TimestampedModel):
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.PositiveSmallIntegerField(
        _("Rating"), blank=True, default=1, validators=[MaxValueValidator(5), MinValueValidator(1)]
    )

    def __str__(self):
        return f"{self.user}: {self.beer} - {self.rating}"

    @staticmethod
    def calculate_rating(beer):
        return BeerRating.objects.filter(beer=beer).aggregate(rating=Avg("rating")).get("rating")

    @staticmethod
    def calculate_rating_count(beer):
        return BeerRating.objects.filter(beer=beer).count()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        beer_rating = super().save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )
        self.beer.rating = self.calculate_rating(self.beer)
        self.beer.rating_count = self.calculate_rating_count(self.beer)
        self.beer.save(update_fields=["rating", "rating_count"])
        return beer_rating


class UserFavorite(TimestampedModel):
    beer = models.ForeignKey(Beer, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def calculate_favorite_count(beer):
        return UserFavorite.objects.filter(beer=beer).count()

    def delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)
        self.beer.favorites_count = self.calculate_favorite_count(self.beer)
        self.beer.save(update_fields=["favorites_count"])
        return

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        favorite = super().save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )
        self.beer.favorites_count = self.calculate_favorite_count(self.beer)
        self.beer.save(update_fields=["favorites_count"])
        return favorite
