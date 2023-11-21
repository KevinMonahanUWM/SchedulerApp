from django.test import TestCase, Client
from TAScheduler.models import User

class SuccessfulLogin(TestCase):
    client = None
    def setUp(self):
        self.client = Client()
        User.objects.create_user(email_address="user@example.com", password="password")

    def test_login_with_valid_credentials(self):
        response = self.client.post('/', {'email': 'user@example.com', 'password': 'password'})
        self.assertRedirects(response, '/home/')  # Assuming the user is redirected to home page on successful login
class InvalidLoginIncorrectPassword(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(email_address="user@example.com", password="password")
    def test_login_with_incorrect_password(self):
        response = self.client.post('/', {'email': 'user@example.com', 'password': 'wrongpassword'})
        self.assertFormError(response, 'form', None, 'Invalid username or password')  # Assuming this error is shown
    def test_login_with_empty_password(self):
        response = self.client.post('/', {'email': 'user@example.com', 'password': ''})
        self.assertFormError(response, 'form', None, 'Password field cannot be empty')
class InvalidLoginNonexistentUser(TestCase):
    def setUp(self):
        self.client = Client()
    def test_login_with_nonexistent_user(self):
        response = self.client.post('/', {'email': 'nonexistent@example.com', 'password': 'password'})
        self.assertFormError(response, 'form', None, 'Invalid username or password')  # Assuming this error is shown
    def test_login_with_empty_username(self):
        response = self.client.post('/', {'email': '', 'password': 'password'})
        self.assertFormError(response, 'form', None, 'Username field cannot be empty')
    def test_login_with_empty_username_and_password(self):
        response = self.client.post('/', {'email': '', 'password': ''})
        self.assertFormError(response, 'form', None, 'Username and Password fields cannot be empty')