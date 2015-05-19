# -*- coding: utf-8 -*-

import hashlib
import hmac
import os.path
import random
import sys
import time

from dolmen.view import ModelView
from .. import View, name, adapts, provides, MultiAdapter, getSession
from skimpyGimpy import skimpyAPI
from zope.interface import Interface
from cromlech.browser.interfaces import ITraverser
from cromlech.webob.response import Response


# Restricted set to avoid 0/o/O or i/I/1 confusion
CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'

SESSION_KEY = 'uvclight.captcha'
WORDLENGTH = 7
FONTPATH = os.path.join(os.path.dirname(__file__), 'tektite.bdf')
SECRET = "CHANGEME"


_TEST_TIME = None


def digest(secret, *args):
    assert len(args) > 1, u'Too few arguments'
    challenge = hmac.new(secret, str(args[0]), hashlib.sha1)
    for arg in args[1:]:
        challenge.update(str(arg))
    return challenge.hexdigest()


class CaptchaSessionHandler(object):
    
    @staticmethod
    def generate_words():
        """Create words for the current session

        We generate one for the current 5 minutes, plus one for the previous
        5. This way captcha sessions have a livespan of 10 minutes at most.

        """
        session = getSession()
        ssid = session[SESSION_KEY]
        nowish = int((_TEST_TIME or time.time()) / 300)
        seeds = [
            digest(SECRET, session, nowish),
            digest(SECRET, session, nowish - 1)]

        words = []
        for seed in seeds:
            word = []
            for i in range(WORDLENGTH):
                index = ord(seed[i]) % len(CHARS)
                word.append(CHARS[index])
            words.append(''.join(word))
        return words

    @staticmethod
    def purge():
        """Set the session cookie
        """
        session = getSession()
        if SESSION_KEY in session:
            del session[SESSION_KEY]

    @staticmethod
    def generate(session_id):
        """Create a new session id
        """
        if session_id is None:
            value = hashlib.sha1(str(random.randrange(sys.maxint))).hexdigest()
            session_id = value
        return session_id

    @classmethod
    def verify(session_id):
        """Ensure session id and cookie exist
        """
        session = getSession()
        if not SESSION_KEY in session:
            session_id = cls.generate(session_id)
            session[SESSION_KEY] = session_id
        return session_id
    

class RenderedCaptcha(ModelView):

    content_type = None
    responseFactory = Response
    _session_id = None
    
    def __init__(self, context, request, word):
        self.context = context
        self.request = request
        self.word = word
        
    def make_response(self, result):
        response = self.responseFactory()
        CaptchaSessionHandler.verify(self._session_id)
        response.setHeader('content-type', self.content_type)
        response.setHeader('cache-control', 'no-cache, no-store')
        response.setHeader('pragma', 'no-cache')
        response.setHeader('expires', 'now')
        return response


class ImageCaptcha(RenderedCaptcha):
    """Image version of the captcha.
    """
    content_type = 'image/png'

    def render(self):
        return skimpyAPI.Png(self.word, speckle=0.5, fontpath=FONTPATH).data()


CAPTCHA_RENDERERS = {
    'image.png': ImageCaptcha,
    }


class CaptchaView(View):
    name('captcha')
    context(Interface)

    _session_id = None
    
    def _url(self, filename):
        return '%s/++captcha++/%s' % (self.url(self.context), filename)

    def image_tag(self):
        self._session_id = CaptchaSessionHandler.verify(self._session_id)
        return '<img src="%s" alt="captcha"/>' % (self._url('image.png'),)

    def verify(self, input):
        if not input:
            return False
        result = False
        try:
            for word in CaptchaSessionHandler.generate_words():
                result = result or input.upper() == word.upper()
            # Delete the session key, we are done with this captcha
            CaptchaSessionHandler.purge()
        except KeyError:
            pass  # No cookie

        return result


class Captcha(MultiAdapter):
    name('captcha')
    adapts(Interface, Interface)
    provides(ITraverser)

    _session_id = None
    
    def travserse(self, ns, name):
        if name in CAPTCHA_RENDERERS:
            CaptchaSessionHandler.verify(self._session_id)
            return CAPTCHA_RENDERERS[name](
                self.context,
                self.request,
                CaptchaSessionHandler.generate_words()[0])
        raise KeyError(name)
