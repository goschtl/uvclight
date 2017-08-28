# -*- coding: utf-8 -*-

import os
from grokcore.component import global_adapter, adapts, name
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import WidgetExtractor
from dolmen.forms.ztk.widgets import choice
from fanstatic import Resource, Library
from js.jquery import jquery
from zope.component import getMultiAdapter
from zope.interface import Interface
from dolmen.forms.ztk.widgets.choice import ChoiceSchemaField
from dolmen.forms.ztk.interfaces import ICollectionField
from dolmen.forms.base.interfaces import IWidget
from dolmen.forms.ztk.fields import SchemaField, SchemaFieldWidget
from dolmen.forms.ztk.widgets.collection import (
    CollectionSchemaField, newCollectionWidgetFactory, MultiChoiceFieldWidget)

from ..directives import adapts, name, context
from ..utils import get_template
from .fields import CaptchaSchemaField, OptionalChoiceField, OrderedChoicesField


widget_library = Library('uvclight', 'static')
optchoice = Resource(widget_library, 'choice.js', depends=[jquery])
multiselectjs = Resource(widget_library, 'multiselect/js/jquery.multi-select.js', depends=[jquery])
multiselect = Resource(widget_library, 'multiselect/css/multi-select.css', depends=[multiselectjs])


class CaptchaFieldWidget(SchemaFieldWidget):
    adapts(CaptchaSchemaField, Interface, Interface)

    template = get_template('captchafieldwidget.cpt', __file__)
    
    def __init__(self, component, form, request):
        super(CaptchaFieldWidget, self).__init__(component, form, request)
        captcha_view = getMultiAdapter((form.context, request), name='captcha')
        self.captcha = captcha_view.image_tag()


class CaptchaWidgetExtractor(WidgetExtractor):
    adapts(CaptchaSchemaField, Interface, Interface)

    def extract(self):
        value, errors = super(CaptchaWidgetExtractor, self).extract()
        if errors:
            return (None, errors)
        if value is not NO_VALUE:
            value = str(value)
            captcha = getMultiAdapter(
                (self.form.context, self.request), name='captcha')
            if not captcha.verify(value):
                return (None, u"Der eingegebene Sicherheitscode ist falsch.")
            return (value, None)
        return (value, None)


class OptionalChoiceFieldWidget(choice.ChoiceFieldWidget):
    adapts(OptionalChoiceField, Interface, Interface)
    template = get_template('optionalchoicefieldwidget.pt')

    def update(self):
        super(OptionalChoiceFieldWidget, self).update()
        optchoice.need()

    def selectValue(self):
        value = self.inputValue()
        if isinstance(value, list):
            return value[0]
        return value

    @property
    def textValue(self):
        value = self.inputValue()
        if isinstance(value, list):
            value = value[1]
        try:
            self.choices().getTermByToken(value)
            return ''
        except:
            return value

    def valueToUnicode(self, value):
        try:
            term = self.choices().getTerm(value)
            return term.token
        except LookupError:
            return value


class OptionalChoiceDisplayWidget(OptionalChoiceFieldWidget):
    name('display')
    template = get_template('optionalchoicedisplaywidget.pt')


class OptionalChoiceWidgetExtractor(WidgetExtractor):
    adapts(OptionalChoiceField, Interface, Interface)

    def extract(self):
        value, error = super(OptionalChoiceWidgetExtractor, self).extract()
        if value == '':
            value = NO_VALUE
            input = None
        else:
            value, input = value
        if input:
            return (input, error)
        if value is not NO_VALUE:
            choices = self.component.getChoices(self.form)
            try:
                value = choices.getTermByToken(value).value
            except LookupError:
                return (None, u'Bitte geben Sie hier einen gültigen Wert ein.')
        return (value, error)


class InOutWidget(MultiChoiceFieldWidget, SchemaFieldWidget):
    adapts(OrderedChoicesField, ChoiceSchemaField, Interface, Interface)

    template = get_template('inout.pt', __file__)

    def htmlClass(self):
        return 'field-list field-inout'

    def __init__(self, field, value_field, form, request):
        super(InOutWidget, self).__init__(field, value_field, form, request)
        multiselect.need()


class OrderedChoicesWidgetExtractor(WidgetExtractor):
    adapts(OrderedChoicesField, ChoiceSchemaField, Interface, Interface)

    def __init__(self, field, value_field, form, request):
        super(OrderedChoicesWidgetExtractor, self).__init__(
            field, form, request)
        self.source = value_field

    def extract(self):
        value = self.request.form.get(self.identifier, NO_VALUE)
        if value is NO_VALUE:
            return (self.component.collectionType(), None)
        choices = self.source.getChoices(self.form)
        try:
            if not isinstance(value, list):
                value = [value]
            value = self.component.collectionType(
                [choices.getTermByToken(t).value for t in value])
        except LookupError:
            return (None, _(u'The selected value is not available.'))

        return (value, None)
