from django.test import TestCase, Client

from TAScheduler.models import User, Administrator


class SuccessfulCreate(TestCase):
    user = None
    account = None
    info = None

    def setUp(self):
        self.user = Client()
        temp = User(email_address="testadmin@uwm.edu", password="pass", first_name="Test", last_name="Test",
                    home_address="Random location", phone_number=9990009999)
        temp.save()
        self.account = Administrator(user=temp)
        self.account.save()
        self.info = {"email_address", "test@uwm.edu", "password", "pass", "first_name", "test", "last_name", "ignore",
                     "home_address", "3400 N Maryland Ave", "phone_number", 4142292222, "role", "TA"}

    # TODO need to make tests work with sessions but I am unsure of how to start that
    def test_creation(self):
        self.user.post("/home/manageaccount/create", self.info)
        self.assertTrue(User.objects.filter(email_address="test@uwm.edu").count() is 1)


class ExistingAccount(TestCase):
    user = None
    account = None
    info = None

    def setUp(self):
        self.user = Client()
        temp = User(email_address="testadmin@uwm.edu", password="pass", first_name="Test", last_name="Test",
                    home_address="Random location", phone_number=9990009999)
        temp.save()
        self.account = Administrator(user=temp)
        self.account.save()
        self.info = {"email_address", "testadmin@uwm.edu", "password", "pass", "first_name", "test", "last_name",
                     "ignore", "home_address", "3400 N Maryland Ave", "phone_number", 4142292222, "role", "TA"}

    # TODO need to make tests work with sessions but I am unsure of how to start that
    def test_existing_user(self):
        resp = self.user.post("/home/manageaccount/create", self.info)
        self.assertEquals(resp.context["message"], "Duplicate User",
                          "You created an account that already exists")


class MissingInformation(TestCase):
    user = None
    account = None
    info = None

    def setUp(self):
        self.user = Client()
        temp = User(email_address="testadmin@uwm.edu", password="pass", first_name="Test", last_name="Test",
                    home_address="Random location", phone_number=9990009999)
        temp.save()
        self.account = Administrator(user=temp)
        self.account.save()
        self.info = {"email_address", "test@uwm.edu", "password", "pass", "first_name", "test", "last_name", "ignore",
                     "home_address", "3400 N Maryland Ave", "phone_number", 4142292222, "role", "TA"}

    # TODO need to make tests work with sessions but I am unsure of how to start that
    def test_one_input(self):
        resp = self.user.post("/home/manageaccount/create", {"role", "TA"})
        self.assertEquals(resp.context["message"], "Missing Information",
                          "You created an account with not all fields filled out")

    def test_six_input(self):
        resp = self.user.post("/home/manageaccount/create",
                              {"password", "pass", "first_name", "test", "last_name", "ignore",
                               "home_address", "3400 N Maryland Ave", "phone_number", 4142292222, "role", "TA"})
        self.assertEquals(resp.context["message"], "Missing Information",
                          "You created an account with not all fields filled out")


class InvalidFormatting(TestCase):
    user = None
    account = None
    info = None

    def setUp(self):
        self.user = Client()
        temp = User(email_address="testadmin@uwm.edu", password="pass", first_name="Test", last_name="Test",
                    home_address="Random location", phone_number=9990009999)
        temp.save()
        self.account = Administrator(user=temp)
        self.account.save()
        self.info = {"email_address", "test@uwm.edu", "password", "pass", "first_name", "test", "last_name", "ignore",
                     "home_address", "3400 N Maryland Ave", "phone_number", 4, "role", "TA"}

    # TODO need to make tests work with sessions but I am unsure of how to start that
    def test_bad_phone(self):
        resp = self.user.post("/home/manageaccount/create", self.info)
        self.assertEquals(resp.context["message"], "Invalid Phone Number",
                          "You created an account with an incorrect phone number")
