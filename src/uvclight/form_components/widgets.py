# -*- coding: utf-8 -*-

from .fields import CaptchaSchemaField, OptionalChoiceField
from zope.component import getMultiAdapter
from ..directives import adapts, name, context
from ..utils import  get_template
from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import WidgetExtractor
from dolmen.forms.ztk.widgets import choice
from dolmen.forms.ztk.fields import SchemaFieldWidget
from fanstatic import Resource, Library
from js.jquery import jquery
from zope.interface import Interface


widget_library = Library('uvclight', 'static')
optchoice = Resource(widget_library, 'choice.js', depends=[jquery])


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
