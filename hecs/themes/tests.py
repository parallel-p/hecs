from django.test import TestCase, RequestFactory
from .models import *
from .views import login_page, signup_page
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware

def add_session_to_request(request):
    """Annotate a request object with a session"""
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

class TestSignup(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_common(self):
        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'firstname': 'f', 'lastname': 'l'})
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
        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'firstname': 'f', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        signup_page(request)
        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'firstname': 'f', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        self.assertEqual(signup_page(request).url.split('?')[-1], 'login_used')
        
class TestLogin(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_common(self):
        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'firstname': 'f', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        signup_page(request)
        request = self.factory.post('/login', {'login': 'l', 'password': 'p'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        response = login_page(request)
        self.assertEqual(response.url, '/')
        
    
    def test_wrong_pass(self):
        request = self.factory.post('/signup', {'login': 'l', 'password': 'p', 'firstname': 'f', 'lastname': 'l'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        signup_page(request)
        request = self.factory.post('/login', {'login': 'l', 'password': 'not_p'})
        request.user = AnonymousUser()
        add_session_to_request(request)
        response = login_page(request)
        self.assertEqual(login_page(request).url.split('?')[-1], 'login_error')