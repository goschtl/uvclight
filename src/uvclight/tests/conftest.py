# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import pytest
import uvclight.tests.examples
from uvclight.tests.testing import configure


@pytest.fixture(scope="session")
def config(request):
    return configure(request, uvclight.tests.examples, 'configure.zcml')

