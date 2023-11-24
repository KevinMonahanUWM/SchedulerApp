import datetime
from django.test import TestCase
from TAScheduler.models import Course, User, TA, Section, Lab, Administrator
from TAScheduler.views_methods import UserObj, CourseObj, AdminObj, TAObj, LabObj, SectionObj

# PBI Assignments ...
# Alec = #1,#2 (Total = 6)
# Kevin = #3,#4,#5 (Total = 4)
# Randall = #6,#7,#8 (Total = 12)
# Kiran = #9,#10,#11 (Total = 15)
# Joe = #12,#13 (Total = 8)
# SEE METHOD DESCRIPTIONS FOR GUIDE ON HOW TO WRITE.
# Feel free to make suggestions on discord (add/remove/edit methods)!.
### Rememeber: These methods were made before any coding (I was guessing) so it's likely they should be changed.
class TestUserLogin(TestCase): # Alec
    def setUp(self):
        user_info = User.objects.create(
            email_address="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            home_address="123 Street",
            phone_number=1234567890
        )
        self.userObj = UserObj(user_info)

    def test_login_valid_credentials(self):
        result = self.userObj.login("test@example.com", "password123")
        self.assertTrue(result)

    def test_login_invalid_credentials(self):
        result = self.userObj.login("test@example.com", "wrongpassword")
        self.assertFalse(result)
class TestUserGetID(TestCase): # Alec
    def setUp(self):
        user_info = User.objects.create(
            email_address="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            home_address="123 Street",
            phone_number=1234567890
        )
        self.userObj = UserObj(user_info)

    def test_get_id(self):
        user_id = self.userObj.getUsername()
        self.assertEqual(user_id, "test@example.com")
class TestUserGetPassword(TestCase): # Alec
    def setUp(self):
        user_info = User.objects.create(
            email_address="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            home_address="123 Street",
            phone_number=1234567890
        )
        self.userObj = UserObj(user_info)

    def test_get_password(self):
        self.assertEqual(self.userObj.getPassword(), "password123")
class TestUserGetName(TestCase): # Alec
    def setUp(self):
        user_info = User.objects.create(
            email_address="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            home_address="123 Street",
            phone_number=1234567890
        )
        self.userObj = UserObj(user_info)
    def test_get_name(self):
        self.assertEqual(self.userObj.getName(), "Test User")
class TestUserGetRole(TestCase): # Alec
    def setUp(self):
        user_info = User.objects.create(
            email_address="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            home_address="123 Street",
            phone_number=1234567890
        )
        self.userObj = UserObj(user_info)
    def test_get_role(self):
        self.assertEqual(self.userObj.getRole(), "user")  # Replace "user" with the actual role name if different
class TestAdminInit(TestCase): # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_model = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_model)
    def test_admin_init(self):
        self.assertEqual(self.adminObj.user.email_address, "admin@example.com")
class TestAdminCreateCourse(TestCase): # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_model = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_model)
        course_info = {
            'course_id': 101,
            'semester': 'Fall 2023',
            'name': 'Intro to Testing',
            'description': 'A course about unit testing',
            'num_of_sections': 3,
            'modality': 'Online',
            'credits': 4
        }
        self.courseObj = CourseObj(course_info)
    def test_create_course(self):
        created_course = self.adminObj.createCourse(self.courseObj)
        self.assertIsNotNone(created_course)
        self.assertEqual(created_course.name, 'Intro to Testing')
class TestAdminCreateUser(TestCase): # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_model = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_model)

    def test_create_user(self):
        user_info = {
            'email_address': 'newuser@example.com',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User',
            'home_address': '123 New Street',
            'phone_number': 9876543210
        }
        created_user = self.adminObj.createUser(user_info)
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email_address, 'newuser@example.com')
class TestAdminCreateSection(TestCase): # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="adminpassword",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_model = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_model)

        self.course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Intro to Django Testing',
            description='A comprehensive course on testing in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )
        section_info = {
            'section_id': 201,
            'course': self.course,
            'location': 'Room 101',
            'meeting_time': datetime.datetime.now()
        }
        self.sectionObj = SectionObj(section_info)  # Assuming SectionObj takes section_info

    def test_create_section(self):
        created_section = self.adminObj.createSection(self.sectionObj)
        self.assertIsNotNone(created_section)
        self.assertEqual(created_section.section_id, 201)

class TestAdminRemoveCourse(TestCase):  # Kevin
    pass


class TestAdminRemoveAccount(TestCase):  # Kevin
    pass


class TestAdminRemoveSection(TestCase):  # Kevin
    pass


class TestAdminEditCourse(TestCase):  # Kevin
    pass


class TestAdminEditSection(TestCase):  # Kevin
    pass


class TestAdminEditAccount(TestCase):  # Kevin
    pass


class TestAdminCourseInstrAsgmt(TestCase):  # Kevin
    pass


class TestAdminCourseTAAsgmt(TestCase):  # Kevin
    pass

class TestTAInit(TestCase):
    pass

class TestTAHasMaxAsgmts(TestCase):  # Kiran
    pass


class TestTAAssignTACourse(TestCase):  # Kiran
    pass


class TestTAGetTACrseAsgmts(TestCase):  # Kiran
    pass


class TestAssignTALab(TestCase):
    pass


class TestTAGetTALabAsgmts(TestCase):  # Kiran
    pass


class TestAssignTALec(TestCase):
    pass


class TestTAGetTALecAsgmts(TestCase):  # Kiran
    pass


class TestTAGetGraderStatus(TestCase):  # Kiran
    pass

class TestInstrutorInit(TestCase):
    pass


class TestInstructorHasMaxAsgmts(TestCase):  # Kiran
    pass


class TestInstructorAssignInstrCourse(TestCase):  # Kiran
    pass


class TestInstructorGetInstrCrseAsgmts(TestCase):  # Kiran
    pass


class TestInstructorAssignInstrLec(TestCase):  # Kiran
    pass


class TestInstructorGetInstrLecAsgmts(TestCase):  # Kiran
    pass


class TestInstructorLecTAAsmgt(TestCase):
    pass


class TestInstructorLabTAAsmgt(TestCase):
    pass

class TestCourseInit(TestCase):
    pass


class TestCourseAddInstructor(TestCase):  # Randall
    pass


class TestCourseAddTA(TestCase):  # Randall
    pass


class TestCourseRemoveAssignment(TestCase):  # Randall
    pass


class TestCourseRemoveCourse(TestCase):  # Randall
    pass


class TestCourseEditCourseInfo(TestCase):  # Randall
    pass


class TestCourseGetAsgmtsForCrse(TestCase):  # Randall
    pass


class TestCourseGetSectionsForCrse(TestCase):  # Randall
    pass


class TestCourseGetCrseInfo(TestCase):  # Randall
    pass


class TestSectionGetID(TestCase):  # Joe
    pass


class TestSectionGetParentCourse(TestCase):  # Joe
    pass


class TestLabInit(TestCase):
    pass

class TestLabGetLabTAAsgmt(TestCase):  # Joe
    pass


class TestLabAddTA(TestCase):  # Joe
    pass


class TestLabRemoveTA(TestCase):  # Joe
    pass


class TestLectureInit(TestCase):
    pass

class TestLectureGetLecInstrAsgmt(TestCase):  # Joe
    pass


class TestLectureAddInstructor(TestCase):  # Joe
    pass


class TestLectureRemoveInstructor(TestCase):  # Joe
    pass


class TestLectureGetLecTAAsgmt(TestCase):  # Joe
    pass


class TestLectureAddTA(TestCase):  # Joe
    pass


class TestLectureRemoveTA(TestCase):  # Joe
    pass
