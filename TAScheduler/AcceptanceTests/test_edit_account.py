from django.test import TestCase, Client

from TAScheduler.models import User, Administrator, TA


class SuccessfulEdit(TestCase):
    user = None
    account = None
    info = None
    tempUser = None

    def setUp(self):
        self.user = Client()
        temp = User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                   last_name="Test",
                                   home_address="Random location", phone_number=9990009999)
        self.account = Administrator.objects.create(user=temp)
        ses = self.user.session
        ses["user"] = str(self.account)
        ses.save()
        temp = User.objects.create(email_address="test@uwm.edu", password="pass", first_name="test", last_name="ignore",
                                   home_address="3400 N Maryland Ave", phone_number=4142292222)
        self.tempUser = TA.objects.create(user=temp, grader_status=False)

    def test_success_change(self):
        self.user.post("/home/manageaccount/", {"user": str(self.tempUser), "edit": "Edit"}, follow=True)
        self.user.post("/home/manageaccount/edit/", {"email_address": "",
                                                    "password": "",
                                                    "first_name": "Paul",
                                                    "last_name": "",
                                                    "home_address": "",
                                                    "phone_number": "",
                                                    "grader_status": "",
                                                    "max_assignments": ""})
        print(User.objects.all())
        self.assertEquals("Paul", User.objects.get(email_address=self.tempUser.user.email_address).first_name,
                          "Did not successfully edit account")


class InvalidFormatting(TestCase):
    user = None
    account = None
    info = None
    tempUser = None

    def setUp(self):
        self.user = Client()
        temp = User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                   last_name="Test",
                                   home_address="Random location", phone_number=9990009999)
        self.account = Administrator.objects.create(user=temp)
        ses = self.user.session
        ses["user"] = str(self.account)
        ses.save()
        temp = User.objects.create(email_address="test@uwm.edu", password="pass", first_name="test", last_name="ignore",
                                   home_address="3400 N Maryland Ave", phone_number=4142292222)
        self.tempUser = TA.objects.create(user=temp, grader_status=False)

    def test_formatting_error(self):
        self.user.post("/home/manageaccount/", {"user": self.tempUser, "edit": "Edit"}, follow=True)
        resp = self.user.post("/home/manageaccount/edit/", {"email_address": "",
                                                           "password": "",
                                                           "first_name": "",
                                                           "last_name": "",
                                                           "home_address": "",
                                                           "phone_number": "414",
                                                           "grader_status": "",
                                                           "max_assignments": ""})
        self.assertEquals(str(resp.context["message"]), "phone_number expects an int input with a length of 10",
                          "Changed phone number to value that does not match standard format")

    def test_formatting_error_ensure_no_change(self):
        self.user.post("/home/manageaccount/", {"user": self.tempUser, "edit": "Edit"}, follow=True)
        resp = self.user.post("/home/manageaccount/edit/", {"email_address": "",
                                                           "password": "",
                                                           "first_name": "",
                                                           "last_name": "",
                                                           "home_address": "",
                                                           "phone_number": "414",
                                                           "grader_status": "",
                                                           "max_assignments": ""})
        self.assertEqual(self.tempUser.user.phone_number, 4142292222,
                         "User was changed when it should still be the same")

