from django.test import TestCase, Client

from TAScheduler.models import User, Administrator


class SuccessfulCreate(TestCase):
    user = None
    account = None

    def setUp(self):
        self.user = Client()
        temp = User(email_address="test@uwm.edu", password="pass", first_name="Test", last_name="Test",
                    home_address="Random location", phone_number=9990009999)
        temp.save()
        self.account = Administrator(user=temp)
        self.account.save()

    def test_creation(self):
        resp = self.user.post("/", {"username", self.account.user.getEmail(), "password", self.account.user.getPass()},
                              follow=True)
        print(resp)
        self.assertTrue(True)

class ExistingAccount(TestCase):
    pass


class MissingInformation(TestCase):
    pass


class InvalidFormatting(TestCase):
    pass
