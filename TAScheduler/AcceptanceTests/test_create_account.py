from django.test import TestCase, Client

from TAScheduler.models import User, Administrator


class SuccessfulCreate(TestCase):
    user = None
    account = None
    info = None

    def setUp(self):
        self.user = Client()
        temp = User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                   last_name="Test",
                                   home_address="Random location", phone_number=9990009999)
        self.account = Administrator.objects.create(user=temp)
        ses = self.user.session
        ses["user"] = str(self.account)
        ses.save()
        self.info = {"email_address": "paul@uwm.edu", "password": "pass", "first_name": "test", "last_name": "ignore",
                     "home_address": "3400 N Maryland Ave", "phone_number": 4142292222, "role": "TA",
                     "grader_status": True}

    def test_creation(self):
        self.user.post("/home/manageaccount/create/", self.info)
        self.assertTrue(User.objects.filter(email_address="paul@uwm.edu").count() is 1, "User should have been created")

    def test_creation_message(self):
        resp = self.user.post("/home/manageaccount/create/", self.info)
        self.assertEquals(resp.context["message"], "User successfully created",
                          "Success message should have displayed")


class ExistingAccount(TestCase):
    user = None
    account = None
    info = None

    def setUp(self):
        self.user = Client()
        temp = User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                   last_name="Test",
                                   home_address="Random location", phone_number=9990009999)
        self.account = Administrator.objects.create(user=temp)
        ses = self.user.session
        ses["user"] = str(self.account)
        ses.save()
        self.info = {"email_address": "testadmin@uwm.edu", "password": "pass", "first_name": "test",
                     "last_name": "ignore",
                     "home_address": "3400 N Maryland Ave", "phone_number": 4142292222, "role": "TA",
                     "grader_status": True}

    def test_existing_user(self):
        resp = self.user.post("/home/manageaccount/create/", self.info)
        self.assertEquals(str(resp.context["message"]), 'User with this email address already exists',
                          "You created an account that already exists")

    def test_existing_user_count(self):
        num_of_users = User.objects.count()
        self.user.post("/home/manageaccount/create/", self.info)
        self.assertEquals(num_of_users, User.objects.count(),
                          "The number of users should not have changed")


class MissingInformation(TestCase):
    user = None
    account = None
    info = None

    def setUp(self):
        self.user = Client()
        temp = User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                   last_name="Test",
                                   home_address="Random location", phone_number=9990009999)
        self.account = Administrator.objects.create(user=temp)
        ses = self.user.session
        ses["user"] = str(self.account)
        ses.save()
        self.info = {"email_address": "testadmin@uwm.edu", "password": "pass", "first_name": "test",
                     "last_name": "ignore",
                     "home_address": "3400 N Maryland Ave", "phone_number": 4142292222, "role": "TA",
                     "grader_status": True}

    def test_one_input(self):
        info = {"email_address": "paul@uwm.edu", "password": "", "first_name": "test",
                "last_name": "ignore",
                "home_address": "3400 N Maryland Ave", "phone_number": 4142292222, "role": "TA",
                "grader_status": True}
        resp = self.user.post("/home/manageaccount/create/", info)
        self.assertEquals(str(resp.context["message"]), "Not all inputs have been provided",
                          "You created an account with not all fields filled out")


class InvalidFormatting(TestCase):
    user = None
    account = None
    info = None

    def setUp(self):
        self.user = Client()
        temp = User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                   last_name="Test",
                                   home_address="Random location", phone_number=9990009999)
        self.account = Administrator.objects.create(user=temp)
        ses = self.user.session
        ses["user"] = str(self.account)
        ses.save()
        self.info = {"email_address": "paul@uwm.edu", "password": "pass", "first_name": "test",
                     "last_name": "ignore",
                     "home_address": "3400 N Maryland Ave", "phone_number": 4, "role": "TA",
                     "grader_status": True}

    def test_bad_phone(self):
        resp = self.user.post("/home/manageaccount/create/", self.info)
        self.assertEquals(str(resp.context["message"]), "phone_number expects an int input with a length of 10",
                          "You created an account with an incorrect phone number")
