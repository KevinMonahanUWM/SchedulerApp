from django.test import TestCase, Client

from TAScheduler.models import User, Administrator, TA


class SuccessfulDelete(TestCase):
    user = None
    account = None
    info = None
    tempUser = None

    def setUp(self):
        self.user = Client()
        temp = User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test", last_name="Test",
                    home_address="Random location", phone_number=9990009999)
        self.account = Administrator.objects.create(user=temp)
        ses = self.user.session
        ses["user"] = str(self.account)
        ses.save()
        temp = User.objects.create(email_address="test@uwm.edu", password="pass", first_name="test", last_name="ignore",
                    home_address="3400 N Maryland Ave", phone_number=4142292222)
        self.tempUser = TA.objects.create(user=temp, grader_status=False)

    def test_correct_delete(self):
        resp = self.user.post("/home/manageaccount/", {"user": str(self.tempUser), "delete": "Delete"})
        self.assertNotIn(self.tempUser.user, User.objects.all(), "Did not successfully delete user")

    def test_correct_delete_message(self):
        resp = self.user.post("/home/manageaccount/", {"user": str(self.tempUser), "delete": "Delete"})
        self.assertEquals(resp.context["message"], "User successfully deleted",
                          "Success message should have displayed")

