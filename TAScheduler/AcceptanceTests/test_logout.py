from django.test import TestCase, Client
from TAScheduler.models import User

class LogoutTest(TestCase):
    client = None
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
        self.client.login(username='testuser', password='12345')

    def test_logout(self):
        # User is logged in here
        response = self.client.get('/home/')  # Assuming /logout/ is the URL for the logout view
        self.assertRedirects(response, '/')  # Assuming user is redirected to login page after logout

        # Check if the user session has been cleared
        self.assertNotIn('_auth_user_id', self.client.session)

