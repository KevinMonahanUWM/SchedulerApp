from datetime import datetime

from TAScheduler.models import User, Administrator, TA, Instructor, Course, InstructorToCourse, Section, Lab
from TAScheduler.views_methods import AdminObj
from django.test import TestCase


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
        user = User.objects.create(
            email_address='test@example.com',
            password='safe_password',
            first_name='Test',
            last_name='User',
            home_address='123 Main St',
            phone_number=1234567890
        )

        # Create a TA or Administrator object and associate it with the User
        self.ta = TA.objects.create(user=user, grader_status=True, max_assignments=3)

    def test_edit_contact_info(self):
        # Use TA's user to update contact info
        self.ta.user.edit_contact_info(first_name='UpdatedName')
        self.ta.user.save()

        updated_user = User.objects.get(id=self.ta.user.id)
        self.assertEqual(updated_user.first_name, 'UpdatedName')


class UserGetContactInfoTest(TestCase):

    def setUp(self):
        # Create a User object
        user = User.objects.create(
            email_address='test@example.com',
            password='safe_password',
            first_name='Test',
            last_name='User',
            home_address='123 Main St',
            phone_number=1234567890
        )

        # Create a TA or Administrator object and associate it with the User
        self.ta = TA.objects.create(user=user, grader_status=True, max_assignments=3)

    def test_get_contact_info(self):
        # Use TA's user to get contact info
        contact_info = self.ta.user.get_contact_info()

        self.assertEqual(contact_info['first_name'], self.ta.user.first_name)
        self.assertEqual(contact_info['last_name'], self.ta.user.last_name)
        self.assertEqual(contact_info['email_address'], self.ta.user.email_address)
        self.assertEqual(contact_info['home_address'], self.ta.user.home_address)
        self.assertEqual(contact_info['phone_number'], self.ta.user.phone_number)


class GetAllUserAssignmentsTest(TestCase):
    def setUp(self):
        # Create user, instructor, course, and assignment instances for testing
        self.user = User.objects.create(
            email_address='instructor@example.com',
            password='safe_password',
            first_name='Instruct',
            last_name='Tor',
            home_address='321 Uni St',
            phone_number=1234567890
        )
        self.instructor = Instructor.objects.create(
            user=self.user,
            max_assignments=3
        )
        self.course = Course.objects.create(
            course_id=101,
            semester='Fall',
            name='Intro to Testing',
            description='A course on testing software',
            num_of_sections=1,
            modality='Online',
        )
        InstructorToCourse.objects.create(
            instructor=self.instructor,
            course=self.course
        )

        # Create TA objects
        self.tas = []
        for i in range(3):  # Create 3 TAs
            ta_user = User.objects.create(
                email_address=f'ta{i}@example.com',
                password='safe_password',
                first_name=f'TA{i}',
                last_name='User',
                home_address='123 TA St',
                phone_number=1234567890 + i
            )
            ta = TA.objects.create(user=ta_user, grader_status=True, max_assignments=6)
            self.tas.append(ta)

        # Assign TAs to sections
        self.sections = []
        for i in range(3):  # Create 3 sections
            section = Section.objects.create(
                section_id=100 + i,
                course=self.course,
                location=f'location{i}',
                meeting_time=datetime(2023, 1, 1 + i, 12, 0, 0)
            )
            self.sections.append(section)
            # Assign TA to a Lab or Lecture
            Lab.objects.create(section=section, ta=self.tas[i % len(self.tas)])

    def test_get_all_assignments(self):
        assignments = self.instructor.get_all_assignments()  # Method call
        self.assertTrue(assignments.exists())
        self.assertEqual(assignments.first().course, self.course)
