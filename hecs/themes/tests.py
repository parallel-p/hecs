from django.test import TestCase, RequestFactory
from .models import *
from .views import login_page, signup_page, blank_page
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from unittest.mock import MagicMock

def add_session_to_request(request):
    """Annotate a request object with a session"""
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

class TestSignup(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_common(self):
        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'password_1': 'p', 'firstname': 'f', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        signup_page(request)
        user = authenticate(username='l', password='p')
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, 'f')
        self.assertEqual(user.last_name, 'l')
        response = signup_page(request)  # already logged in
        self.assertEqual(response.url, '/')
    
    def test_login_busy(self):
        User.objects.create_user('l', password='p', first_name='f', last_name='l').save()
        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'password_1': 'p', 'firstname': 'f1', 'lastname': 'l1'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        self.assertEqual(signup_page(request).url.split('?')[-1], 'login_used')

    def test_missing(self):
        request = self.factory.post('/signup', {'login': '', 'password': 'p', 'password_1': 'p', 'firstname': 'f', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        self.assertEqual(signup_page(request).url.split('?')[-1], 'missing')

        request = self.factory.post('/signup', {'login': 'l', 'password': '', 'password_1': 'p', 'firstname': 'f', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        self.assertEqual(signup_page(request).url.split('?')[-1], 'missing')

        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'password_1': '', 'firstname': 'f', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        self.assertEqual(signup_page(request).url.split('?')[-1], 'missing')

        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'password_1': 'p', 'firstname': '', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        self.assertEqual(signup_page(request).url.split('?')[-1], 'missing')

        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'password_1': 'p', 'firstname': 'f', 'lastname': ''})
        request.user = AnonymousUser()
        add_session_to_request(request)
        self.assertEqual(signup_page(request).url.split('?')[-1], 'missing')

    def test_passwords_not_match(self):
        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'password_1': 'q', 'firstname': 'f', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        self.assertEqual(signup_page(request).url.split('?')[-1], 'passwords_not_match')

        
class TestLogin(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_common(self):
        User.objects.create_user('l', password='p', first_name='f', last_name='l').save()
        request = self.factory.post('/login', {'login': 'l', 'password': 'p'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        response = login_page(request)
        self.assertEqual(response.url, '/')
        
    
    def test_wrong_pass(self):
        User.objects.create_user('l', password='p', first_name='f', last_name='l').save()
        request = self.factory.post('/login', {'login': 'l', 'password': 'not_p'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        response = login_page(request)
        self.assertEqual(login_page(request).url.split('?')[-1], 'login_error')

class TestBlank(TestCase):
    def test_1(self):
        theme = Theme()
        theme.name = 'sqr'
        theme.save()
        theme = Theme()
        theme.name = 'sqrt'
        theme.save()
        theme = Theme()
        theme.name = 'sqrl'
        theme.save()

        user = User.objects.create_user('l', password='p', first_name='f', last_name='l')
        user.save()

        request = RequestFactory().post('/blank', {'sqrt': '2', 'sqr': '3', 'sqrl': ''})
        request.user = user
        add_session_to_request(request)
        blank_page(request)
        print(list(Blank.objects.filter(user=request.user).all()))
        for blank in list(Blank.objects.filter(user=request.user).all()):
            if blank.theme.name == 'sqrt' and blank.result != '2':
                self.assertEqual(blank.result, '2')
            elif blank.theme.name == 'sqr' and blank.result != '3':
                self.assertEqual(blank.result, '3')
            elif blank.theme.name != 'sqr' and blank.theme.name != 'sqrt':
                self.assertEqual(blank.result, '')

        self.assertTrue(True)