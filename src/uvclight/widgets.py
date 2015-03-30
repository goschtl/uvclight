import datetime

from dolmen.forms.base.markers import NO_VALUE
from dolmen.forms.base.widgets import WidgetExtractor
from dolmen.forms.ztk.fields import registerSchemaField
from dolmen.forms.ztk.widgets import choice
from dolmen.forms.ztk.widgets.choice import ChoiceFieldWidget
from zope.event import notify
from zope.interface import Interface
from zope.schema import Choice
from js.jquery import jquery
from fanstatic import Resource, Library

from .directives import adapts, implementer, name
from .utils import  get_template


widget_library = Library('uvclight', 'static')
optchoice = Resource(widget_library, 'choice.js', depends=[jquery])


class IOptionalChoice(Interface):
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
                return (None, u'Invalid value')
        return (value, error)


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
