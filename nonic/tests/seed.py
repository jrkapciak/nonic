import factory
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker
from faker.providers import company

from nonic import models

faker = Faker()
faker.add_provider(company)


class BeerStyleFactory(DjangoModelFactory):
    class Meta:
        model = models.Style
        get_or_crate = "name"


name = factory.LazyAttribute(lambda obj: faker.lexify())


class ManufacturerFactory(DjangoModelFactory):
    class Meta:
        model = models.Manufacturer
        get_or_crate = "name"


name = factory.LazyAttribute(lambda obj: faker.company())


class BeerFactory(DjangoModelFactory):
    class Meta:
        model = models.Beer
        get_or_crate = "code"

    name = factory.LazyAttribute(lambda obj: faker.company())
    code = faker.ean()
    description = faker.paragraph(variable_nb_sentences=False)
    manufactured_by = SubFactory(ManufacturerFactory)
    volume = faker.random_int()
    tags = faker.json()

    @factory.post_generation
    def style(self, create, styles, **kwargs):
        if not create:
            return

        if styles:
            for style in styles:
                self.style.add(style)
