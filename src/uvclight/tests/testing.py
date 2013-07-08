# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import os

from zope.component.hooks import setHooks
from zope.configuration import xmlconfig, config
from zope.testing.cleanup import cleanUp


def configure(request, module, zcml):
    request.addfinalizer(cleanUp)
    return setup_config(module, zcml)


def setup_config(package, zcml_file):
    zcml_file = os.path.join(os.path.dirname(package.__file__),
                             zcml_file)
    setHooks()
    context = config.ConfigurationMachine()
    xmlconfig.registerCommonDirectives(context)

    return xmlconfig.file(zcml_file,
                          package=package,
                          context=context, execute=True)
