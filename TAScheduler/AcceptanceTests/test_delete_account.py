from django.test import TestCase, Client

from TAScheduler.models import User, Administrator, TA


class SuccessfulDelete(TestCase):
    user = None
    account = None
    info = None
    tempUser = None

    def setUp(self):
        self.user = Client()
        temp = User(email_address="testadmin@uwm.edu", password="pass", first_name="Test", last_name="Test",
                    home_address="Random location", phone_number=9990009999)
        temp.save()
        self.account = Administrator(user=temp)
        self.account.save()
        self.tempUser = User(email_address="test@uwm.edu", password="pass", first_name="test", last_name="ignore",
                    home_address="3400 N Maryland Ave", phone_number=4142292222)
        self.tempUser.save()
        TA(user=self.tempUser).save()

    def test_correct_delete(self):
        self.user.post("/home/manageaccount/delete", {"selection", self.tempUser})
        self.assertNotIn(self.tempUser, User.objects, "Did not successfully delete user")


class NoUsers(TestCase):
    user = None

    def setUp(self):
        self.user = Client()

    def test_no_users(self):
        resp = self.user.get("/home/manageaccount/delete")
        self.assertEquals(resp.context["message"], "No existing users to delete", "Cannot go to delete accounts when "
                                                                                  "there are no users")
