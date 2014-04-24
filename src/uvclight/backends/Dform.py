try:
    from deform import Button, Form, ValidationFailure
    from uvclight import View, Page

    
    class Action(Button):

        def extractData(self, form, control_items):
            return form.validate(control_items)
        
        def __call__(self, view, form, data):
            validated = self.extractData(form, data.items())
            return validated
            

    class Form(object):
        handler = Form
        actions = set()
        schema = None
        use_ajax = False
        ajax_options = dict()

        def __init__(self, context, request):
            self.context = context
            self.request = request

        def render(self):
            form = self.handler(
                self.schema, buttons=self.actions,
                use_ajax=self.use_ajax, ajax_options=str(self.ajax_options))

            for button in self.actions:
                if button.name in self.request.form:
                    try:
                        validated = button(self, form, self.request.form)
                    except ValidationFailure, e:
                        return e.render()
                    else:
                        return u'OK'
            return form.render()


    class FormView(Form, View):
        pass


    class FormPage(Form, Page):
        pass


except ImportError:
    raise
    #pass
