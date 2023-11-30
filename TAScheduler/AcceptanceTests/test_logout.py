from django.test import TestCase, Client
from TAScheduler.models import User, Administrator


class LogoutTest(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        temp = User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                   last_name="Test",
                                   home_address="Random location", phone_number=9990009999)
        self.account = Administrator.objects.create(user=temp)
        ses = self.client.session
        ses["user"] = str(self.account)
        ses.save()

    def test_logout(self):
        # User is logged in here
        response = self.client.post('/home/', {"logout": "logout"})  # Assuming /logout/ is the URL for the logout view
        self.assertRedirects(response, '/')  # Assuming user is redirected to login page after logout

        # Check if the user session has been cleared
        self.assertNotIn("user", self.client.session)
