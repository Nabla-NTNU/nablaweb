"""
Splash - Tests
"""

from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory

from splash.middleware import SplashMiddleware
from splash.models import SplashConfig

import logging
log = logging.getLogger(__name__)

class SplashMiddlewareTestCase(TestCase):
    """
    Tests for the splash screen app middleware
    """

    def setUp(self):
        """
        Init
        """
        self.splash_middleware = SplashMiddleware()
        self.request_factory = RequestFactory(SERVER_NAME='example.org')
        SplashConfig().save()

    def build_request(self, username=None, cookies=None, url_path='/somewhere'):
        """
        Builds a new request, associated with a user (anonymous by default)
        """
        request = self.request_factory.get(url_path)

        if username is None:
            request.user = AnonymousUser()
        else:
            request.user = User.objects.create_user(username, 'test@example.com', username)

        if cookies is not None:
            request.COOKIES = cookies

        return request

    def assert_redirect(self, response, redirect_url):
        """
        Check that the response redirects to `redirect_url`, without requiring client
        interface on the response object
        """
        self.assertTrue(response)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'], redirect_url)

    def test_feature_disabled(self):
        """
        No redirect when the feature is disabled
        """
        request = self.build_request()
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    def test_no_cookie(self):
        """
        No cookie present should redirect
        """
        SplashConfig(
            enabled=True,
        ).save()

        request = self.build_request()
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')

    def test_wrong_cookie(self):
        """
        A cookie value different from the allowed ones should redirect
        """
        SplashConfig(
            enabled=True,
            cookie_allowed_values='ok1,ok2',
            redirect_url='http://example.com'
        ).save()

        request = self.build_request(cookies={'edx_splash_screen': 'not ok'})
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://example.com')

    def test_right_cookie(self):
        """
        A cookie value corresponding to one of the allowed ones should not redirect
        """
        SplashConfig(
            enabled=True,
            cookie_allowed_values='ok1,ok2',
            redirect_url='http://example.com'
        ).save()

        request = self.build_request(cookies={'edx_splash_screen': 'ok2'})
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    def test_wrong_cookie_different_cookie_name(self):
        """
        Different cookie name
        A cookie value different from the allowed ones should redirect
        """
        SplashConfig(
            enabled=True,
            cookie_name='othername',
        ).save()

        request = self.build_request(cookies={'othername': 'not ok'})
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')

    def test_right_cookie_different_cookie_name(self):
        """
        Different cookie name
        A cookie value corresponding to one of the allowed ones should not redirect
        """
        SplashConfig(
            enabled=True,
            cookie_name='othername',
        ).save()

        request = self.build_request(cookies={'othername': 'seen'})
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    def test_not_unaffected_user(self):
        """
        Setting unaffected users should still redirect other users
        """
        SplashConfig(
            enabled=True,
            unaffected_usernames='user1',
        ).save()

        request = self.build_request(username='user2')
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')

    def test_unaffected_user(self):
        """
        Unaffected users should never be redirected
        """
        SplashConfig(
            enabled=True,
            unaffected_usernames='user1',
        ).save()

        request = self.build_request(username='user1')
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    def test_redirect_to_current_url(self):
        """
        When the URL of the redirection is the same as the current URL,
        we shouldn't be redirected
        """
        SplashConfig(
            enabled=True,
            redirect_url='http://example.org/somewhere'
        ).save()

        request = self.build_request()
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    def test_set_non_absolute_url(self):
        """
        Make sure the URL is absolute, to make sure we can compare it
        to the current URL
        Should not validate with a non-absolute URL
        """
        config = SplashConfig(redirect_url='/somewhere')
        self.assertRaises(ValidationError, config.save)

    def test_unaffected_path(self):
        """
        Unaffected paths should never be redirected - custom value
        """
        SplashConfig(
            enabled=True,
            unaffected_url_paths='/test1,/my/url/',
        ).save()

        request = self.build_request(url_path='/my/url/')
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

    def test_unaffected_wildcard_path(self):
        """
        Unaffected wildcard paths should never be redirected - custom value
        """
        SplashConfig(
            enabled=True,
            unaffected_url_paths='/test1/*, /test2/*/after, /test3/*/before/*/after',
        ).save()

        # These paths match and should NOT redirect.
        request = self.build_request(url_path='/test1/')
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)
        request = self.build_request(url_path='/test1/something')
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)
        request = self.build_request(url_path='/test1/something/else')
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)
        request = self.build_request(url_path='/test2/something/after')
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)
        request = self.build_request(url_path='/test3/something/before/something/else/after')
        response = self.splash_middleware.process_request(request)
        self.assertEquals(response, None)

        # These paths don't match and should redirect.
        request = self.build_request(url_path='/test2/')
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')
        request = self.build_request(url_path='/test2/after')
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')
        request = self.build_request(url_path='/test3/before/after')
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')
        request = self.build_request(url_path='/test3/something/before/something/after/more')
        response = self.splash_middleware.process_request(request)
        self.assert_redirect(response, 'http://edx.org')
