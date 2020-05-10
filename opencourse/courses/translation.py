from modeltranslation.translator import register, TranslationOptions
from . import models


@register(models.CourseArea)
class AreaTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.City)
class CityTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.CourseLevel)
class AreaTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.CourseAge)
class AreaTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.CourseLanguage)
class AreaTranslationOptions(TranslationOptions):
    fields = ["name"]


@register(models.CourseLocationType)
class AreaTranslationOptions(TranslationOptions):
    fields = ["name"]
