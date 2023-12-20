from django.test import TestCase, Client
from TAScheduler.models import User, Administrator
from TAScheduler.view_methods.admin_methods import AdminObj


class SuccessfulLogin(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        user = User.objects.create(
            email_address='testuser@example.com',
            password='12345',
            first_name="Test",
            last_name="User",
            home_address="123 Test Street",
            phone_number=1234567890
        )
        AdminObj(Administrator.objects.create(user=user))

    def test_login_with_valid_credentials(self):
        response = self.client.post('/', {'username': 'testuser@example.com', 'password': '12345'}, follow=True)
        print(response.context)
        self.assertRedirects(response, '/home/')  # Assuming the user is redirected to home page on successful login


class InvalidLoginIncorrectPassword(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email_address='testuser@example.com',
            password='12345',
            first_name="Test",
            last_name="User",
            home_address="123 Test Street",
            phone_number=1234567890
        )

    def test_login_with_incorrect_password(self):
        response = self.client.post('/', {'email': 'user@example.com', 'password': 'wrongpassword'})
        self.assertEquals(response.context["error"], 'Invalid username or password')  # Assuming this error is shown

    def test_login_with_empty_password(self):
        response = self.client.post('/', {'email': 'user@example.com', 'password': ''})
        self.assertEquals(response.context["error"], 'Invalid username or password')


class InvalidLoginNonexistentUser(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_with_nonexistent_user(self):
        response = self.client.post('/', {'email': 'nonexistent@example.com', 'password': 'password'})
        self.assertEquals(response.context["error"], 'Invalid username or password')  # Assuming this error is shown

    def test_login_with_empty_username(self):
        response = self.client.post('/', {'email': '', 'password': 'password'})
        self.assertEquals(response.context["error"], 'Invalid username or password')

    def test_login_with_empty_username_and_password(self):
        response = self.client.post('/', {'email': '', 'password': ''})
        self.assertEquals(response.context["error"], 'Invalid username or password')
