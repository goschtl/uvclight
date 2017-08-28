# -*- coding: utf-8 -*-

from .interfaces import ICaptcha, IOptionalChoice, IOrderedChoices
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.ztk.fields import SchemaField
from dolmen.forms.ztk.fields import registerSchemaField
from dolmen.forms.ztk.widgets import choice
from zope.interface import implementer
from zope.schema import ASCIILine, Choice, List
from dolmen.forms.ztk.widgets.collection import CollectionSchemaField, makeCollectionSchemaFactory


@implementer(IOrderedChoices)
class OrderedChoices(List):
    pass


@implementer(ICaptcha)
class Captcha(ASCIILine):
    pass


class CaptchaSchemaField(SchemaField):

    def validate(self, value, form):
        return None


class OrderedChoicesField(CollectionSchemaField):
    pass
    

@implementer(IOptionalChoice)
class OptionalChoice(Choice):
    """A choice field with the option to add an alternative value
    """
    def __init__(self, values=None, vocabulary=None,
                 source=None, **kw):
        Choice.__init__(self, values, vocabulary, source, **kw)

    def _validate(self, value):
        if self._init_field:
            return
        return


class OptionalChoiceField(choice.ChoiceField):

    def validate(self, value, form):
        return None


def OptionalChoiceSchemaFactory(schema):
    field = OptionalChoiceField(
        schema.title or None,
        identifier=schema.__name__,
        description=schema.description,
        required=schema.required,
        readonly=schema.readonly,
        source=schema.vocabulary,
        vocabularyName=schema.vocabularyName,
        interface=schema.interface,
        defaultValue=schema.default or NO_VALUE)
    return field


def register():
    registerSchemaField(OptionalChoiceSchemaFactory, IOptionalChoice)
    registerSchemaField(CaptchaSchemaField, ICaptcha)
    registerSchemaField(makeCollectionSchemaFactory(OrderedChoicesField), IOrderedChoices)
