from modeltranslation.translator import translator, TranslationOptions
from .models import Beer, Style


class BeerTranslationOptions(TranslationOptions):
    fields = ("description",)


class StyleTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(Beer, BeerTranslationOptions)
translator.register(Style, StyleTranslationOptions)
