from unittest import TestCase

from TAScheduler.models import Administrator, User, Section, Course, Instructor, TA
from TAScheduler.views_methods import AdminObj, TAObj


class TestUserLogin(TestCase):  # Alec
    admin_user_info = None
    admin_info = None
    result = None

    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="admin_pass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_info = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_info)

    def test_login_valid_credentials(self):
        result = self.adminObj.login("admin@example.com", "admin_pass")
        self.assertTrue(result, "login with valid credentials failed")

    def test_login_invalid_credentials(self):
        # Assuming the login method returns False for invalid credentials
        result = self.adminObj.login("admin@example.com", "wrong_password")
        self.assertFalse(result, "login with invalid credentials should fail but didn't")

    def test_login_wrong_username(self):
        result = self.adminObj.login("wrong@example.com", "admin_pass")
        self.assertFalse(result, "login with wrong username and correct password should fail but didn't")

    def test_login_no_input(self):
        result = self.adminObj.login("", "")
        self.assertFalse(result, "login with no credentials should fail but didn't")


class TestUserGetUsername(TestCase):  # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="admin_pass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_info = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_info)

    def test_get_username(self):
        user_id = self.adminObj.getUsername()
        self.assertEqual(user_id, "admin@example.com", msg="user.getUsername failed to return username")


class TestUserGetPassword(TestCase):  # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="admin_pass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_info = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_info)

    def test_get_password(self):
        self.assertEqual(self.adminObj.getPassword(), "admin_pass", msg="user.getPassword failed to retrieve password")


class TestUserGetName(TestCase):  # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="admin_pass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_info = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_info)

    def test_get_name(self):
        user_name = self.adminObj.getName()
        self.assertEqual(user_name, "Admin User", msg="user.getName failed to return name")


class TestUserGetRole(TestCase):  # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="admin_pass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_info = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_info)

    def test_get_role(self):
        self.assertEqual(self.adminObj.getRole(), "Admin", msg="user.getRole failed to retrieve 'admin'")

class UserEditMyContactInfoTest(TestCase):

    def setUp(self):
        # Create a User object
        self.user = User.objects.create(
            email_address='test@example.com',
            password='safe_password',
            first_name='Test',
            last_name='User',
            home_address='123 Main St',
            phone_number=1234567890
        )
        # Create a TA or Administrator object and associate it with the User
        self.ta = TA.objects.create(user=self.user, grader_status=True, max_assignments=3)

    def test_edit_contact_info(self):
        ta_obj = TAObj(self.ta)
        ta_obj.editContactInfo(first_name='UpdatedName')

        updated_user = User.objects.get(id=self.ta.user.id)
        self.assertEqual(updated_user.first_name, 'UpdatedName')

    def test_duplicate_email_update(self):
        User.objects.create(
            email_address='other@example.com',
            password='safe_password',
            first_name='Other',
            last_name='User',
            home_address='456 Main St',
            phone_number=9876543210
        )
        ta_obj = TAObj(self.ta)
        with self.assertRaises(RuntimeError):
            ta_obj.editContactInfo(email_address='other@example.com')

    def test_invalid_phone_number_update(self):
        ta_obj = TAObj(self.ta)
        with self.assertRaises(ValueError):
            ta_obj.editContactInfo(phone_number='invalid_phone')


class UserGetContactInfoTest(TestCase):

    def setUp(self):
        # Creating user and TA objects
        self.user = User.objects.create(email_address="ta@example.com", password="password123",
                                        first_name="TAFirstName", last_name="TALastName", home_address="TA Address",
                                        phone_number=1234567890)
        self.ta = TA.objects.create(user=self.user, grader_status=True, max_assignments=3)

        # Creating instructor user and object
        self.instructor_user = User.objects.create(email_address="instructor@example.com", password="password456",
                                                   first_name="InstructorFirstName", last_name="InstructorLastName",
                                                   home_address="Instructor Address", phone_number=9876543210)
        self.instructor = Instructor.objects.create(user=self.instructor_user, max_assignments=3)

        # Creating course and sections
        self.course = Course.objects.create(course_id=123, semester="Fall", name="Sample Course",
                                            description="A sample course", num_of_sections=2, modality="Online")
        self.section = Section.objects.create(section_id=456, course=self.course, location="Room 101",
                                              meeting_time="2023-09-01 09:00")

    def test_get_contact_info(self):
        # Create a TAObj instance using the TA instance
        ta_obj = TAObj(self.ta)

        # Use TAObj's get_contact_info method to retrieve contact info
        contact_info = ta_obj.getContactInfo()

        # Assert the retrieved contact information is as expected
        self.assertEqual(contact_info['first_name'], self.ta.user.first_name)
        self.assertEqual(contact_info['last_name'], self.ta.user.last_name)
        self.assertEqual(contact_info['email_address'], self.ta.user.email_address)
        self.assertEqual(contact_info['home_address'], self.ta.user.home_address)
        self.assertEqual(contact_info['phone_number'], self.ta.user.phone_number)