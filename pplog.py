#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import functools
from pit import Pit  # from github
from selenium.webdriver import Firefox as WebDriver
from zope.interface import (
    Attribute,
    Interface,
    implementer,
    )
from zope.component import (
    createObject,
    getGlobalSiteManager,
    )
from zope.component.interfaces import IFactory


@implementer(IFactory)
class PPLogBackendBrowserFactory(object):
    def __init__(self):
        self._target = None

    def __call__(self):
        if self._target is None:
            self._target = PPLogBackendBrowser()
            self._target.start()
        return self._target


class PPLogBackendBrowser(object):
    def __init__(self):
        self._browser = None

    def start(self):
        print('START')
        secret = createObject('pplog.secret')
        # desired_capabilities={'phantomjs.page.settings.userAgent': ""})
        self._browser = WebDriver()
        self._browser.implicitly_wait = 10  # pageをloadするまでの待ち時間を設定
        # browser.delete_allcookies()  # Cookieを全消し
        self._browser.get('https://pplog.net/')
        time.sleep(1)
        self._browser.get('https://pplog.net/users/auth/twitter')
        self._browser.find_element_by_id('username_or_email').send_keys(secret.username)
        self._browser.find_element_by_id('password').send_keys(secret.password)
        self._browser.find_element_by_css_selector('.submit').click()

    def post(self, *args, **kwds):
        print('POST')
        for ii in range(100):  # retry count
            print('COUNT: {}'.format(ii))
            try:
                self._post(*args, **kwds)
            except:
                self._browser.get('https://www.pplog.net/')
            else:
                self._browser.get('https://www.pplog.net/')
                break
            time.sleep(1)
        else:
            print('retry error')

    def _post(self, data):
        time.sleep(1)
        self._browser.find_element_by_css_selector('.new-btn').click()
        form = self._browser.find_element_by_css_selector('form#new_post_')
        form.find_element_by_tag_name('textarea').send_keys(data)
        time.sleep(1)
        form.find_element_by_css_selector('input.btn-primary').click()
        print('OK')


class ISecret(Interface):
    username = Attribute(u'')
    password = Attribute(u'')


@implementer(ISecret)
class PPlogSecret(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password


@implementer(IFactory)
class PPLogSecretFactory(object):
    @functools.lru_cache()
    def __call__(self):
        conf = Pit.get('pplog', {'require': {
            'username': '',
            'password': '',
        }})
        return PPlogSecret(
            username=conf['username'],
            password=conf['password'],
            )


def includeme(config):
    registry = getGlobalSiteManager()
    registry.registerUtility(PPLogBackendBrowserFactory(), IFactory, 'pplog')
    registry.registerUtility(PPLogSecretFactory(), IFactory, 'pplog.secret')
