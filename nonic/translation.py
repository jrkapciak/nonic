from modeltranslation.translator import TranslationOptions, translator

from .models import Beer, Style


class BeerTranslationOptions(TranslationOptions):
    fields = ("description",)


class StyleTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(Beer, BeerTranslationOptions)
translator.register(Style, StyleTranslationOptions)
