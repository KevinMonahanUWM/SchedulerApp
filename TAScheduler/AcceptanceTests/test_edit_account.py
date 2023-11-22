from django.test import TestCase, Client

from TAScheduler.models import User, Administrator, TA


class SuccessfulEdit(TestCase):
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
        TA(user=self.tempUser, grader_status=False).save()

    def test_success_change(self):
        self.user.post("/home/manageaccount/edit", {"User", self.tempUser}, follow=True)
        self.user.post("/home/manageaccount/edit", {"first_name", "Paul"})
        self.assertEquals("Paul", User.objects.get(self.tempUser), "Did not successfully edit account")


class InvalidFormatting(TestCase):
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
        TA(user=self.tempUser, grader_status=False).save()

    def test_formatting_error(self):
        self.user.post("/home/manageaccount/edit", {"User", self.tempUser}, follow=True)
        resp = self.user.post("/home/manageaccount/edit", {"phone_number", 414})
        self.assertEquals(resp.context["message"], "BAD PHONE NUMBER: must be 10 digit int", "Changed phone number to "
                                                                                             "value that does not "
                                                                                             "match standard format")

    def test_formatting_error_ensure_no_change(self):
        self.user.post("/home/manageaccount/edit", {"User", self.tempUser}, follow=True)
        resp = self.user.post("/home/manageaccount/edit", {"phone_number", 414})
        self.assertIn(self.tempUser, User.objects, "User was changed when it should still be the same")


class DiscardChanges(TestCase):
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

    def test_discard(self):
        resp = self.user.post('/home/manageaccount/edit', {"discard", True}, follow=True)
        self.assertRedirects(resp, "/home/manageaccount/edit", status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True,
                             msg="Discard changes did not redirect back to edit main page")
        self.assertIn(self.account.user, User.objects, "User was changed when it should still be the same")


class NoUsers(TestCase):
    user = None

    def setUp(self):
        self.user = Client()

    def test_no_users(self):
        resp = self.user.get("/home/manageaccount/edit")
        self.assertEquals(resp.context["message"], "No existing users to delete", "Cannot go to delete accounts when "
                                                                                  "there are no users")
