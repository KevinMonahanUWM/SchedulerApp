from datetime import datetime

from django.test import TestCase
from TAScheduler.models import Course, User, TA, Section, Lab, Administrator, InstructorToCourse, TAToCourse, \
    Instructor, Lecture

from django.core.exceptions import ValidationError

from TAScheduler.view_methods.admin_methods import AdminObj
from TAScheduler.view_methods.course_methods import CourseObj
from TAScheduler.view_methods.instructor_methods import InstructorObj
from TAScheduler.view_methods.lab_methods import LabObj
from TAScheduler.view_methods.lecture_methods import LectureObj
from TAScheduler.view_methods.ta_methods import TAObj


# Don't need to fix these imports, will need to change the separated ones


# SEE METHOD DESCRIPTIONS FOR GUIDE ON HOW TO WRITE.
# Feel free to make suggestions on discord (add/remove/edit methods)!.
# Remember: These methods were made before any coding (I was guessing) so it's likely they should be changed.

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


class TestAdminInit(TestCase):  # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="admin_pass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_model = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_model)
        self.course_info = {
            "course_id": 101,
            "semester": 'Fall 2023',
            "name": 'Intro to Testing',
            "description": 'A course about unit testing',
            "num_of_sections": 3,
            "modality": 'Online',
        }

    def test_create_course(self):
        created_course = self.adminObj.createCourse(self.course_info)
        self.assertIsNotNone(created_course)
        self.assertEqual(created_course.name, 'Intro to Testing', msg="failed to create course")

    def test_admin_init(self):
        self.assertEqual(self.adminObj.database.user.email_address, "admin@example.com",
                         msg="failed to initialize admin")


class TestAdminCreateCourse(TestCase):  # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="admin_pass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_model = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_model)
        self.course_info = {
            'course_id': 101,
            'semester': 'Fall 2023',
            'name': 'Intro to Testing',
            'description': 'A course about unit testing',
            'num_of_sections': 3,
            'modality': 'Online',
        }

    def test_create_course(self):
        self.adminObj.createCourse(self.course_info)
        # Checking if the course has been successfully saved in the database
        course_count = Course.objects.filter(course_id=101).count()
        self.assertGreater(course_count, 0, msg="Course not found in the database")


class TestAdminCreateUser(TestCase):  # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="admin_pass",
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
        self.adminObj.createUser(user_info, role='TA')
        user_count = User.objects.filter(email_address='newuser@example.com').count()
        self.assertGreater(user_count, 0, msg="User not found in the database")


class TestAdminCreateSection(TestCase):
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="admin_password",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_model = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_model)

    def test_create_section(self):
        course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Intro to Django Testing',
            description='A comprehensive course on testing in Django.',
            num_of_sections=3,
            modality='Online',
        )
        section_info = {
            'section_id': 201,
            'course': Course.objects.get(course_id=course.course_id),
            'location': 'Room 101',
            'meeting_time': "2000-1-1 12:00:00",
            "section_type": "Lab"
        }
        print(course)
        print(course.course_id)
        print(section_info["course"].course_id)
        self.adminObj.createSection(section_info)

        # Check if the section has been successfully saved in the database
        section_count = Section.objects.filter(section_id=201).count()
        self.assertGreater(section_count, 0, msg="Section not found in the database")


class TestAdminRemoveCourse(TestCase):  # Kevin
    tempCourse = None
    admin = None
    hold_course = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
        )
        self.tempCourse = CourseObj(self.hold_course)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

    def test_successful_delete(self):
        self.admin.removeCourse(self.tempCourse)
        self.assertNotIn(self.hold_course, Course.objects.values(), "Did not remove course from the database")

    def test_delete_null_course(self):
        Course.delete(self.hold_course)
        with self.assertRaises(RuntimeError, msg="Tried to delete a non-existent course"):
            self.admin.removeCourse(self.tempCourse)

    def test_delete_non_course(self):
        with self.assertRaises(TypeError, msg="Tried to delete not a course"):
            self.admin.removeCourse(11)


class TestAdminRemoveAccount(TestCase):  # Kevin
    tempTA = None
    admin = None
    hold_user = None

    def setUp(self):
        self.hold_user = User.objects.create(
            email_address='kev@example.com',
            password='kev_password',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number=1234667890
        )
        temp_ta = TA.objects.create(user=self.hold_user, grader_status=False)
        self.tempTA = TAObj(temp_ta)
        temp = User.objects.create(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_admin = Administrator(user=temp)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

    def test_successful_delete(self):
        self.admin.removeUser(self.tempTA)
        self.assertNotIn(self.hold_user, User.objects.values(), "Did not remove user from the database")

    def test_delete_null_user(self):
        User.delete(self.hold_user)
        with self.assertRaises(RuntimeError, msg="Tried to delete a non-existent user"):
            self.admin.removeUser(self.tempTA)

    def test_delete_non_user(self):
        with self.assertRaises(TypeError, msg="Tried to delete not a user"):
            self.admin.removeUser(11)


class TestAdminRemoveSection(TestCase):  # Kevin
    hold_sec = None
    admin = None
    tempLab = None

    def setUp(self):
        temp_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.hold_sec = Section.objects.create(
            section_id=1011,
            course=temp_course,
            location="A distant realm",
            meeting_time="2000-1-1 12:00:00"
        )
        temp_lab = Lab.objects.create(
            section=self.hold_sec,
            ta=None
        )
        self.tempLab = LabObj(temp_lab)
        temp = User.objects.create(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_admin = Administrator(user=temp)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

    def test_successful_delete(self):
        self.admin.removeSection(self.tempLab)
        self.assertNotIn(self.hold_sec, Section.objects.values(), "Did not remove section from the database")

    def test_delete_null_user(self):
        Section.delete(self.hold_sec)
        with self.assertRaises(RuntimeError, msg="Tried to delete a non-existent section"):
            self.admin.removeSection(self.tempLab)

    def test_delete_non_user(self):
        with self.assertRaises(TypeError, msg="Tried to delete not a section"):
            self.admin.removeSection(11)


class TestAdminEditCourse(TestCase):  # Kevin
    tempCourse = None
    admin = None
    new_info = None

    def setUp(self):
        hold_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.tempCourse = CourseObj(hold_course)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.new_info = {"course_id": 103,
                         "semester": "Spring 2024",
                         "name": "Intro to Units",
                         "description": "Unit testing at its finest",
                         "num_of_sections": 4,
                         "modality": ""}

    def test_bad_course(self):
        with self.assertRaises(TypeError, msg='Course that was passed is not a valid course'):
            self.admin.editCourse(11, self.new_info)

    def test_bad_info(self):
        with self.assertRaises(TypeError, msg='Improper input entered for editing course'):
            self.admin.editCourse(self.tempCourse, 11)

    def test_success(self):
        self.admin.editCourse(self.tempCourse, self.new_info)
        self.assertEqual(self.new_info["description"], Course.objects.get(course_id=103).description)

    def test_bad_item_in_info(self):
        info = {"course_id": 103,
                "semester": "Spring 2024",
                "name": 4,
                "description": "Unit testing at its finest",
                "num_of_sections": "4",
                "modality": ""}
        with self.assertRaises(ValueError, msg='Improper input entered for editing course'):
            self.admin.editCourse(self.tempCourse, info)


class TestAdminEditSection(TestCase):  # Kevin
    tempLab = None
    admin = None
    new_info = None

    def setUp(self):
        hold_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        hold_sec = Section.objects.create(
            section_id=1011,
            course=hold_course,
            location="The end of the universe",
            meeting_time="2000-1-1 12:00:00"
        )
        hold_lab = Lab.objects.create(
            section=hold_sec,
            ta=None
        )
        self.tempLab = LabObj(hold_lab)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.new_info = {"section_id": 1012,
                         "location": "Somewhere in the universe",
                         "meeting_time": "2000-1-1 12:00:00"}

    def test_bad_section(self):
        with self.assertRaises(TypeError, msg='Section that was passed is not a valid section'):
            self.admin.editSection(11, self.new_info)

    def test_bad_info(self):
        with self.assertRaises(TypeError, msg='Improper input entered for editing section'):
            self.admin.editSection(self.tempLab, 11)

    def test_success(self):
        self.admin.editSection(self.tempLab, self.new_info)
        self.assertEqual(self.new_info["location"], Section.objects.get(section_id=1012).location)

    def test_bad_item_info(self):
        info = {"section_id": 1012,
                "location": "",
                "meeting_time": "bad date"}
        with self.assertRaises(ValueError, msg="Should have thrown error with bad input"):
            self.admin.editSection(self.tempLab, info)


class TestAdminEditAccount(TestCase):  # Kevin
    tempTA = None
    admin = None
    new_info = None

    def setUp(self):
        self.hold_user = User.objects.create(
            email_address='kev@example.com',
            password='kev_password',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number=1234667890
        )
        temp_ta = TA.objects.create(user=self.hold_user, grader_status=False)
        self.tempTA = TAObj(temp_ta)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.new_info = {"grader_status": True,
                         "max_assignments": 3,
                         "first_name": "Paul",
                         "last_name": "Different"}

    def test_bad_user(self):
        with self.assertRaises(TypeError, msg='User that was passed is not a valid user'):
            self.admin.editUser(11, self.new_info)

    def test_bad_info(self):
        with self.assertRaises(TypeError, msg='Improper input entered for editing user'):
            self.admin.editUser(self.tempTA, 11)

    def test_success(self):
        self.admin.editUser(self.tempTA, self.new_info)
        self.assertEqual(self.new_info["first_name"], User.objects.get(first_name="Paul").first_name)
        self.assertEqual(self.new_info["grader_status"], TA.objects.get(user=self.tempTA.database.user).grader_status)

    def test_bad_item_info(self):
        info = {"grader_status": "Maybe",
                "max_assignments": 3,
                "first_name": "Paul",
                "last_name": 123}
        with self.assertRaises(ValueError, msg="Should have thrown error with bad input"):
            self.admin.editUser(self.tempTA, info)


class TestAdminCourseInstrAssignment(TestCase):  # Kevin
    tempCourse = None
    tempInstr = None
    admin = None
    hold_course = None
    hold_user = None
    hold_instr = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.tempCourse = CourseObj(self.hold_course)
        self.hold_user = User.objects.create(
            email_address='kev@example.com',
            password='kev_password',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number=1234667890
        )
        self.hold_instr = Instructor.objects.create(user=self.hold_user)
        self.tempInstr = InstructorObj(self.hold_instr)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

    def test_bad_instr(self):
        with self.assertRaises(TypeError, msg='Instructor that was passed is not a valid Instructor'):
            self.admin.courseInstrAsmgt(11, self.tempCourse)

    def test_bad_course(self):
        with self.assertRaises(TypeError, msg='Course that was passed is not a valid course'):
            self.admin.courseInstrAsmgt(self.tempInstr, 11)

    def test_null_instr(self):
        User.delete(self.hold_user)
        with self.assertRaises(RuntimeError, msg="Tried to link course to non existent user"):
            self.admin.courseInstrAsmgt(self.tempInstr, self.tempCourse)

    def test_null_course(self):
        Course.delete(self.hold_course)
        with self.assertRaises(RuntimeError, msg="Tried to link user to non existent course"):
            self.admin.courseInstrAsmgt(self.tempInstr, self.tempCourse)

    def test_success_connect(self):
        self.admin.courseInstrAsmgt(self.tempInstr, self.tempCourse)
        self.assertEqual(InstructorToCourse.objects.get(course=self.hold_course, instructor=self.hold_instr).course,
                         self.hold_course, "Should have linked course and instructor together")

    def test_max_capacity_instr(self):
        User.delete(self.hold_user)
        temp = User.objects.create(
            email_address='kev@example.com',
            password='kev_password',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number=1234667890
        )
        instr = Instructor.objects.create(
            user=temp,
            max_assignments=0
        )
        temp_in = InstructorObj(instr)
        with self.assertRaises(RuntimeError, msg="Tried to link course to instructor with max assignments"):
            self.admin.courseInstrAsmgt(temp_in, self.tempCourse)


class TestAdminCourseTAAssignment(TestCase):  # Kevin
    tempCourse = None
    tempTA = None
    admin = None
    hold_course = None
    hold_user = None
    hold_ta = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.tempCourse = CourseObj(self.hold_course)
        self.hold_user = User.objects.create(
            email_address='kev@example.com',
            password='kev_password',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number=1234667890
        )
        self.hold_ta = TA.objects.create(user=self.hold_user, grader_status=True)
        self.tempTA = TAObj(self.hold_ta)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

    def test_bad_instr(self):
        with self.assertRaises(TypeError, msg='TA that was passed is not a valid TA'):
            self.admin.courseInstrAsmgt(11, self.tempCourse)

    def test_bad_course(self):
        with self.assertRaises(TypeError, msg='Course that was passed is not a valid course'):
            self.admin.courseInstrAsmgt(self.tempTA, 11)

    def test_null_instr(self):
        User.delete(self.hold_user)
        with self.assertRaises(RuntimeError, msg="Tried to link course to non existent user"):
            self.admin.courseTAAsmgt(self.tempTA, self.tempCourse)

    def test_null_course(self):
        Course.delete(self.hold_course)
        with self.assertRaises(RuntimeError, msg="Tried to link user to non existent course"):
            self.admin.courseTAAsmgt(self.tempTA, self.tempCourse)

    def test_success_connect(self):
        self.admin.courseTAAsmgt(self.tempTA, self.tempCourse)
        self.assertEqual(TAToCourse.objects.get(course=self.hold_course, ta=self.hold_ta).course,
                         self.hold_course, "Should have linked course and TA together")

    def test_max_capacity_instr(self):
        User.delete(self.hold_user)
        temp = User.objects.create(
            email_address='kev@example.com',
            password='kev_password',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number=1234667890
        )
        ta = TA.objects.create(
            user=temp,
            max_assignments=0,
            grader_status=False
        )
        temp_ta = TAObj(ta)
        with self.assertRaises(RuntimeError, msg="Tried to link course to TA with max assignments"):
            self.admin.courseTAAsmgt(temp_ta, self.tempCourse)


class TestAdminCourseUserAsgmt(TestCase):
    tempCourse = None
    tempInstr = None
    tempTA = None
    admin = None
    hold_course = None
    hold_instr = None

    def setUp(self):
        hold_user = User.objects.create(
            email_address='ta@example.com',
            password='ta_password',
            first_name='ta',
            last_name='ta',
            home_address='123 ta St',
            phone_number=1234667890
        )
        hold_user.save()
        self.hold_ta = TA.objects.create(user=hold_user, grader_status=True)
        self.tempTA = TAObj(self.hold_ta)

        hold_user = User.objects.create(
            email_address='instr@example.com',
            password='instr_password',
            first_name='instr',
            last_name='instr',
            home_address='123 instr St',
            phone_number=1234667890
        )
        hold_user.save()
        self.hold_instr = Instructor.objects.create(user=hold_user)
        self.tempInstr = InstructorObj(self.hold_instr)

        self.hold_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.tempCourse = CourseObj(self.hold_course)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

    def test_success_intructor(self):
        self.admin.courseUserAsgmt(self.tempInstr, self.tempCourse)
        self.assertIsNotNone(InstructorToCourse.objects.get(instructor=self.hold_instr, course=self.hold_course),
                             "Instructor to Course object not made in AdminCourseUserAsgmt")

    def test_success_ta(self):
        self.admin.courseUserAsgmt(self.tempTA, self.tempCourse)
        self.assertIsNotNone(TAToCourse.objects.get(ta=self.hold_ta, course=self.hold_course),
                             "TA to Course object not made in AdminCourseUserAsgmt")

    def test_bad_user_input(self):
        with self.assertRaises(TypeError, msg="AdminCourseUserAsgmt Does not raise TYPEERROR for bad user"):
            self.admin.courseUserAsgmt("STRING!", self.hold_course)

    def test_bad_course_input_instr(self):
        with self.assertRaises(TypeError,
                               msg="AdminCourseUserAsgmt Does not raise TYPEERROR for bad course when instructor"):
            self.admin.courseUserAsgmt(self.hold_instr, "STRING!")

    def test_bad_course_input_ta(self):
        with self.assertRaises(TypeError, msg="AdminCourseUserAsgmt Does not raise TYPEERROR for bad course when TA"):
            self.admin.courseUserAsgmt(self.hold_ta, "STRING!")


class TestSecTAAsgmt(TestCase):
    admin = None
    ta = None
    section = None

    def setUp(self):
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

        tempcourse = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        tempcourse.save()

        self.section = Section.objects.create(
            section_id=800,
            course=tempcourse,
            location="East Lane",
            meeting_time=datetime(2023, 1, 1, 12, 0, 0)
        )
        self.section.save()

        tmpuser = User.objects.create(
            email_address='ta@example.com',
            password='password',
            first_name='Ta',
            last_name='User',
            home_address='123 TA St',
            phone_number=1234567890
        )
        self.ta = TA.objects.create(
            user=tmpuser,
            grader_status=False
        )

    def test_success_lab(self):
        laboratory = Lab.objects.create(
            section=self.section
        )
        labobj = LabObj(laboratory)
        self.admin.sectionTAAsmgt(self.ta, labobj)
        self.assertEqual(labobj.getLabTAAsgmt(), self.ta, "Did not assign correct laboratory")

    def test_success_lec(self):
        lecture = Lecture.objects.create(
            section=self.section
        )
        lecobj = LectureObj(lecture)
        tmpuser = User.objects.create(
            email_address='ta@example.com',
            password='password',
            first_name='Ta',
            last_name='User',
            home_address='123 TA St',
            phone_number=1234567890
        )
        tmpta = TA.objects.create(
            user=tmpuser,
            grader_status=True
        )
        tmpta.save()
        self.admin.sectionTAAsmgt(tmpta, lecobj)
        self.assertEqual(lecobj.getLectureTAAsgmt(), tmpta, "Did not assign correct lecture")

    def test_bad_ta(self):
        laboratory = Lab.objects.create(
            section=self.section
        )
        labobj = LabObj(laboratory)
        with self.assertRaises(TypeError, msg="Does not raise typerror for bad TA"):
            self.admin.sectionTAAsmgt("String!", labobj)

    def test_bad_section(self):
        with self.assertRaises(TypeError, msg="Does not raise typerror for bad Section"):
            self.admin.sectionTAAsmgt(self.ta, "STRING!")


class TestGetAllCrseAsgmts(TestCase):
    admin = None
    course1 = None
    course2 = None
    ta1 = None
    ta2 = None
    instr1 = None
    instr2 = None

    def setUp(self):
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.course1 = Course.objects.create(
            course_id=104,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.course1.save()
        tempUser = User.objects.create(email_address='ta1@example.com',
                                       password='user_password',
                                       first_name='user',
                                       last_name='User',
                                       home_address='123 user1 St',
                                       phone_number='1234567890')
        self.ta1 = TA.objects.create(user=tempUser, grader_status=False, max_assignments=5)
        self.ta1.save()
        TAToCourse.objects.create(ta=self.ta1, course=self.course1)

        tempUser = User.objects.create(email_address='instr1@example.com',
                                       password='instr_password',
                                       first_name='instr',
                                       last_name='instr',
                                       home_address='123 instr1 St',
                                       phone_number='1234567890')
        self.instr1 = Instructor.objects.create(user=tempUser, max_assignments=5)
        self.instr1.save()
        InstructorToCourse.objects.create(instructor=self.instr1, course=self.course1)

        self.course2 = Course.objects.create(
            course_id=102,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.course2.save()
        tempUser = User.objects.create(email_address='ta2@example.com',
                                       password='user_password',
                                       first_name='user',
                                       last_name='User',
                                       home_address='123 user1 St',
                                       phone_number='1234567890')
        self.ta2 = TA.objects.create(user=tempUser, grader_status=False, max_assignments=5)
        self.ta2.save()
        TAToCourse.objects.create(ta=self.ta2, course=self.course2)

        tempUser = User.objects.create(email_address='instr2@example.com',
                                       password='instr_password',
                                       first_name='instr',
                                       last_name='instr',
                                       home_address='123 instr1 St',
                                       phone_number='1234567890')
        self.instr2 = Instructor.objects.create(user=tempUser, max_assignments=5)
        self.instr2.save()
        InstructorToCourse.objects.create(instructor=self.instr2, course=self.course2)

    def test_successful(self):
        self.assertEqual(TAToCourse.objects.count(), 2, "Did not make the correct amount of links")
        self.assertEqual(InstructorToCourse.objects.count(), 2, "Did not make the correct amount of links")
        self.assertIsInstance(self.admin.getAllCrseAsgmts(), dict, "Does not return dictionary")
        self.assertEqual(self.admin.getAllCrseAsgmts().get(104), ('instr1@example.com', 'ta1@example.com'),
                         "Course 104 does not do")
        self.assertEqual(self.admin.getAllCrseAsgmts().get(102), ('instr2@example.com', 'ta2@example.com'),
                         "Course 102 does not do")
        # IDK what I want it to output as

    def test_no_courses(self):
        TAToCourse.objects.all().delete()
        InstructorToCourse.objects.all().delete()
        with self.assertRaises(RuntimeError, msg="Code does not produce RuntimeError when no crse assignments"):
            self.admin.getAllCrseAsgmts()


class TestAdminGetAllSecAsgmt(TestCase):  # Kiran
    adminObj = None

    def setUp(self):
        tempCourse = Course.objects.create(course_id=1,
                                           semester="fall",
                                           name="course1",
                                           description="#1",
                                           num_of_sections=3,
                                           modality="online")
        for i in [1, 2, 3, 4]:  # ta + sec + lecture
            tempUser = User.objects.create(email_address='user@example.com' + str(i),
                                           password='user_password' + str(i),
                                           first_name='user' + str(i),
                                           last_name='User',
                                           home_address='123 user1 St',
                                           phone_number='1234567890')
            tempTa = TA.objects.create(user=tempUser, grader_status=False, max_assignments=5)
            tempSec = Section.objects.create(section_id=i,
                                             course=tempCourse,
                                             location="EAS",
                                             meeting_time=datetime(2023, 1, 1 + i, 12, 0, 0))
            Lecture.objects.create(section=tempSec, ta=tempTa)
        tempUserDB = User.objects.create(
            email_address='admin@example.com',
            password='adminpass',
            first_name='admin',
            last_name='User',
            home_address='123 admin St',
            phone_number=1234667890
        )
        tempAdminDB = Administrator.objects.create(user=tempUserDB)
        self.adminObj = AdminObj(tempAdminDB)

    # [1] Successfully matched the section assignments with the database
    def test_success(self):
        self.assertQuerysetEqual(Section.objects.all(), self.adminObj.getAllSecAsgmt(), ordered=False,
                                 msg="should have returned all sections")

    # [2] Raise error if no courses
    def test_raiseErrorNoCourse(self):
        Course.objects.all().delete()
        with self.assertRaises(RuntimeError, msg="can't return sections when no courses exists"):
            self.adminObj.getAllSecAsgmt()

    # [3] Raise error if no sections
    def test_raiseErrorNoSec(self):
        Section.objects.all().delete()
        with self.assertRaises(RuntimeError, msg="can't return sections when no sections exists"):
            self.adminObj.getAllSecAsgmt()


class TestTAInit(TestCase):
    database = None
    user = None

    def setUp(self):
        self.user = User.objects.create(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        self.database = TA.objects.create(user=self.user, grader_status=False)

    def test_bad_input(self):
        with self.assertRaises(TypeError, msg='TA that was passed is not a valid TA'):
            TAObj(11)

    def test_null_ta(self):
        User.delete(self.user)
        with self.assertRaises(TypeError, msg='TA that was passed does not exist'):
            TAObj(self.database)

    def test_success(self):
        ta = TAObj(self.database)
        self.assertEqual(ta.database, self.database,
                         "TA object should be saved in the database reference")


class TestTAHasMaxAssignments(TestCase):  # Kiran
    taDB = None
    courseDB = None
    user = None  # for TA
    taObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number=1234567890
        )
        self.taDB = TA.objects.create(user=self.user, grader_status=False, max_assignments=1)  # max 1 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database.
        temp_userForAdmin = User.objects.create(email_address='admin@example.com',
                                                password='admin_password',
                                                first_name='Admin',
                                                last_name='User',
                                                home_address='123 Admin St',
                                                phone_number=1234567890)
        tempAdmin = Administrator.objects.create(user=temp_userForAdmin)
        self.adminObj = AdminObj(tempAdmin)

        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )

    # [1] TA w/ 1 course assignment
    def test_1Course1MaxCap(self):
        TAToCourse.objects.create(ta=self.taDB, course=self.courseDB)  # assigning TA to course using db?
        self.assertEqual(self.taObj.hasMaxAsgmts(), True,
                         msg="TA has 1 max assignments & assigned 1 course: @ max cap")

    # [2] TA w/ 0 course assignment
    def test_0Course1MaxCap(self):
        self.assertEqual(self.taObj.hasMaxAsgmts(), False,
                         msg="TA has 1 max assignments & not assigned 1 course: not @ max cap")

    # [3] TA w/ max cap -> no max assign
    # using views method: I know bad practice but this is still a good test to ensure both method's working correctly
    def test_origMaxCapToNoAssignment(self):
        TAToCourse.objects.create(ta=self.taDB, course=self.courseDB)
        self.adminObj.removeCourse(CourseObj(self.courseDB))
        self.assertEqual(self.taObj.hasMaxAsgmts(), False,
                         msg="TA originally w/ assignment, removed, shouldn't be at max cap")


class TestTAGetTALecAssignments(TestCase):  # Kiran
    taDB = None
    user = None  # for TA
    taObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number=1234567890
        )
        self.taDB = TA.objects.create(user=self.user, grader_status=True,
                                      max_assignments=1)  # True gs,max 1 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database.
        temp_userForAdmin = User.objects.create(email_address='admin@example.com',
                                                password='admin_password',
                                                first_name='Admin',
                                                last_name='User',
                                                home_address='123 Admin St',
                                                phone_number=1234567890)
        tempAdmin = Administrator.objects.create(user=temp_userForAdmin)
        self.adminObj = AdminObj(tempAdmin)
        # Course
        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        TAToCourse.objects.create(ta=self.taDB, course=self.courseDB)
        # Section
        self.sectionDB = Section.objects.create(
            section_id=100 + 1,
            course=self.courseDB,
            location="location" + str(1),
            meeting_time=datetime(2023, 1, 1, 12, 0, 0)
        )
        # Lecture - create assignments in the test.

    # [1] 1 lecture assignment
    def test_1Assignment(self):
        Lecture.objects.create(section=self.sectionDB, ta=self.taDB)  # creating assignment?
        self.assertQuerysetEqual(Lecture.objects.filter(ta=self.taDB), self.taObj.getTALecAsgmts(),
                                 msg="should be 1 assigment")

    # [2] 0 lab assignment
    def test_0Assignment(self):
        self.assertQuerysetEqual(Lecture.objects.filter(ta=self.taDB), self.taObj.getTALecAsgmts(),
                                 msg="should be 0 assignments")


class TestTAGetGraderStatus(TestCase):  # Kiran
    taDB1 = None
    taDB2 = None
    taObj1 = None
    taObj2 = None
    userDBList = list()  # just for 2 non/grader status

    def setUp(self):
        for i in [1, 2]:
            self.userDBList.append(User.objects.create(
                email_address='TA@example.com' + str(i),
                password='TA_password',
                first_name='TA',
                last_name='User',
                home_address='123 TA St',
                phone_number=1234567890)
            )
        self.taDB1 = TA.objects.create(user=self.userDBList[0], max_assignments=1, grader_status=True)
        self.taDB2 = TA.objects.create(user=self.userDBList[1], max_assignments=1, grader_status=False)
        self.taObj1 = TAObj(self.taDB1)  # grader
        self.taObj2 = TAObj(self.taDB2)  # non-grader

    # [1] Getting non-grader status
    def test_nonGraderStatus(self):
        self.assertEqual(self.taObj1.getGraderStatus(), True, msg="grader status ta should have true GS field")

    # [2] Getting grader status
    def test_graderStatus(self):
        self.assertEqual(self.taObj2.getGraderStatus(), False, msg="non grader status ta should have false GS field")


class TestTASetSkills(TestCase):  # Kiran
    userDB = None
    taDB = None
    taObj = None

    def setUp(self):
        userDB = User.objects.create(
            email_address='TA@example.com1',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number=1234567890,
        )
        self.taDB = TA.objects.create(user=userDB, grader_status=True, skills="very good")
        self.taDB.save()
        self.taObj = TAObj(self.taDB)

    def test_success(self):
        self.taObj.setSkills("good veryyyy good")
        self.assertEqual(self.taDB.skills, "good veryyyy good",
                         msg="should have changed the skills")

    def test_missingSkills(self):
        with self.assertRaises(TypeError, msg="can't set skills to nothing"):
            self.taObj.setSkills("")

    def test_invalidTypeSkills(self):
        with self.assertRaises(TypeError, msg="can't set skills to non-string"):
            self.taObj.setSkills(10)


class TestInstructorInit(TestCase):
    instructorDB = None
    user = None
    instrObj = None

    def setUp(self):
        self.user = User.objects.create(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        self.instructorDB = Instructor.objects.create(user=self.user, max_assignments=1)

    def test_bad_input(self):
        with self.assertRaises(TypeError, msg='instructor that was passed is not a valid TA'):
            self.instrObj = InstructorObj(11)

    def test_null_Instructor(self):
        User.objects.get(email_address='admin@example.com').delete()
        with self.assertRaises(TypeError, msg='instructor that was passed does not exist'):
            self.instrObj = InstructorObj(self.instructorDB)

    def test_success(self):
        self.instrObj = InstructorObj(self.instructorDB)
        self.assertEqual(self.instrObj.database, self.instructorDB,
                         msg="instructor object should be saved in the database reference")

        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )


class TestInstructorHasMaxAssignments(TestCase):  # Kiran
    instrDB = None
    courseDB = None
    user = None  # for instructor
    instrObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number=1234567890
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.instrObj = InstructorObj(self.instrDB)
        temp_userForAdmin = User.objects.create(email_address='admin@example.com',
                                                password='admin_password',
                                                first_name='Admin',
                                                last_name='User',
                                                home_address='123 Admin St',
                                                phone_number=1234567890)
        tempAdmin = Administrator.objects.create(user=temp_userForAdmin)
        self.adminObj = AdminObj(tempAdmin)
        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )

    # [1] Instr w/ 1 course assignment
    def test_1Course1MaxCap(self):
        InstructorToCourse.objects.create(instructor=self.instrDB, course=self.courseDB)
        self.assertEqual(self.instrObj.hasMaxAsgmts(), True,
                         msg="instructor has 1 max assignments & assigned 1 course: @ max cap")

    # [2] Instr w/ 0 course assignment
    def test_0Course1MaxCap(self):
        self.assertEqual(self.instrObj.hasMaxAsgmts(), False,
                         msg="instructor has 1 max assignments & not assigned 1 course: not @ max cap")

    # [3] Instr w/ max cap -> no max assign
    # using views method
    def test_origMaxCapToNoAssignment(self):
        InstructorToCourse.objects.create(instructor=self.instrDB, course=self.courseDB)
        self.adminObj.removeCourse(
            CourseObj(self.courseDB))  # removing course SHOULD also remove this instructor's assignment
        self.assertEqual(self.instrObj.hasMaxAsgmts(), False,
                         msg="instructor originally w/ assignment, removed, shouldn't be at max cap")


class TestInstructorGetInstrCourseAssignments(TestCase):  # Kiran
    instrDB = None
    courseDB = None
    course = None
    user = None  # for TA
    instrObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='instr@example.com',
            password='instr_password',
            first_name='instr',
            last_name='User',
            home_address='123 instr St',
            phone_number=1234567890
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.instrObj = InstructorObj(self.instrDB)
        temp_userForAdmin = User.objects.create(email_address='admin@example.com',
                                                password='admin_password',
                                                first_name='Admin',
                                                last_name='User',
                                                home_address='123 Admin St',
                                                phone_number=1234567890)
        tempAdmin = Administrator.objects.create(user=temp_userForAdmin)
        self.adminObj = AdminObj(tempAdmin)
        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.course = CourseObj(self.courseDB)

    # [1] 1 assignment
    def test_1Assignment(self):
        InstructorToCourse.objects.create(course=self.courseDB, instructor=self.instrDB)  # creating assignment?
        self.assertQuerysetEqual(InstructorToCourse.objects.filter(instructor=self.instrDB),
                                 self.instrObj.getInstrCrseAsgmts(), msg="should be 1 assigment")

    # [2] 0 assignment
    def test_0Assignment(self):
        self.assertQuerysetEqual(InstructorToCourse.objects.filter(instructor=self.instrDB),
                                 self.instrObj.getInstrCrseAsgmts(), msg="should be 0 assignments")


class TestInstructorGetInstrLecAssignments(TestCase):  # Kiran
    instrDB = None
    lecDB = None
    user = None  # for instructor
    instrObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='Instr@example.com',
            password='Instr_password',
            first_name='Instr',
            last_name='User',
            home_address='123 Instr St',
            phone_number=1234567890
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.instrObj = InstructorObj(self.instrDB)
        temp_userForAdmin = User.objects.create(email_address='admin@example.com',
                                                password='admin_password',
                                                first_name='Admin',
                                                last_name='User',
                                                home_address='123 Admin St',
                                                phone_number=1234567890)
        tempAdmin = Administrator.objects.create(user=temp_userForAdmin)
        self.adminObj = AdminObj(tempAdmin)
        # Course
        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        # Section
        self.sectionDB = Section.objects.create(
            section_id=100 + 1,
            course=self.courseDB,
            location="location" + str(1),
            meeting_time=datetime(2023, 1, 1, 12, 0, 0)
        )
        # Lecture - create assignments in the test.


class TestCourseAddInstructor(TestCase):  # Randall
    hold_course = None
    tempCourse = None
    instructor_user = None
    instructor_model = None
    instructor = None
    instructorObj = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.tempCourse = CourseObj(self.hold_course)
        self.instructor_user = User.objects.create(
            email_address='instructor@example.com',
            password='password',
            first_name='Instructor',
            last_name='User',
            home_address='123 Instructor St',
            phone_number='1234567891'
        )
        self.instructor_model = Instructor.objects.create(
            user=self.instructor_user, max_assignments=1)  # Create an Instructor model instance
        self.instructor = InstructorObj(self.instructor_model)  # Wrap it with InstructorObj

    def test_add_instructor(self):
        self.tempCourse.addInstructor(self.instructor)
        # Check if the instructor was added to the course

        instructor_to_course_exists = InstructorToCourse.objects.filter(
            instructor=self.instructor_model,  # Use the Instructor model instance
            course=self.hold_course
        ).exists()
        self.assertTrue(instructor_to_course_exists, "Instructor was not added to the course")

    def test_add_instructor_at_max_assignments(self):
        self.instructor_model.max_assignments = 0
        self.instructor_model.save()
        with self.assertRaises(ValueError):
            self.tempCourse.addInstructor(self.instructor)

    def test_add_instructor_to_full_course(self):
        # Fill the course with the maximum number of instructors
        for _ in range(self.hold_course.num_of_sections):
            instructor_user = User.objects.create(
                email_address='new_instructor@example.com',
                password='password',
                first_name='New',
                last_name='Instructor',
                home_address='123 Instructor St',
                phone_number='1234567890'  # Include phone number
            )
            instructor_model = Instructor.objects.create(
                user=instructor_user, max_assignments=1
            )
            instructor_obj = InstructorObj(instructor_model)
            self.tempCourse.addInstructor(instructor_obj)

        # Attempt to add another instructor
        extra_instructor_user = User.objects.create(
            email_address='extra_instructor@example.com',
            password='password',
            first_name='Extra',
            last_name='Instructor',
            home_address='456 Instructor Lane',
            phone_number='0987654321'  # Include phone number
        )
        extra_instructor_model = Instructor.objects.create(
            user=extra_instructor_user, max_assignments=1
        )
        extra_instructor_obj = InstructorObj(extra_instructor_model)

        # This should raise ValueError since the course is already full
        with self.assertRaises(ValueError):
            self.tempCourse.addInstructor(extra_instructor_obj)


class TestCourseInit(TestCase):  #
    pass


class TestCourseAddTA(TestCase):  # Randall
    hold_course = None
    tempCourse = None
    TA_user = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=102,
            semester='Spring 2024',
            name='Advanced Testing',
            description='A course about advanced testing methods.',
            num_of_sections=2,
            modality='Hybrid'
        )
        self.tempCourse = CourseObj(self.hold_course)
        self.ta_user = User.objects.create(
            email_address='ta@example.com',
            password='password',
            first_name='TA',
            last_name='Assistant',
            home_address='123 TA St',
            phone_number='1234567892'
        )

        self.ta_model = TA.objects.create(
            user=self.ta_user,
            grader_status=False,
            max_assignments=2  # Assuming this attribute exists
        )
        self.ta = TAObj(self.ta_model)  # Correctly wrap it with TAObj

    def test_add_ta(self):
        self.tempCourse.addTa(self.ta)
        # Check if the TA was added to the course

        ta_to_course_exists = TAToCourse.objects.filter(
            ta=self.ta.database,  # Use the underlying TA database model instance
            course=self.hold_course
        ).exists()
        self.assertTrue(ta_to_course_exists, "TA was not added to the course")

    def test_add_ta_at_max_assignments(self):
        self.ta.database.max_assignments = 0  # Assume max assignments are now full
        self.ta.database.save()
        with self.assertRaises(ValueError):
            self.tempCourse.addTa(self.ta)

    def test_add_ta_to_full_course(self):
        # Fill the course with the maximum number of TAs
        for _ in range(self.hold_course.num_of_sections):
            ta_user = User.objects.create(
                email_address=f'ta{_}@example.com',
                password='password',
                first_name='TA',
                last_name=f'Assistant{_}',
                home_address=f'123 TA St {_}',
                phone_number=f'12345678{_}'
            )
            ta_model = TA.objects.create(
                user=ta_user, max_assignments=1, grader_status=False
            )
            ta_obj = TAObj(ta_model)
            self.tempCourse.addTa(ta_obj)

        # Attempt to add another TA
        extra_ta_user = User.objects.create(
            email_address='extra_ta@example.com',
            password='password',
            first_name='Extra',
            last_name='TA',
            home_address='456 TA Lane',
            phone_number='0987654321'
        )
        extra_ta_model = TA.objects.create(
            user=extra_ta_user, max_assignments=1, grader_status=False
        )
        extra_ta_obj = TAObj(extra_ta_model)

        # This should raise ValueError since the course is already full
        with self.assertRaises(ValueError):
            self.tempCourse.addTa(extra_ta_obj)


class TestCourseRemoveAssignment(TestCase):  # Randall
    hold_course = None
    tempCourse = None
    ta_user = None
    ta_obj = None
    instructor_user = None
    instructor_obj = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=103,
            semester='Summer 2024',
            name='Intermediate Testing',
            description='Intermediate course on testing.',
            num_of_sections=2,
            modality='In-person'
        )
        self.tempCourse = CourseObj(self.hold_course)

        # Create TA
        self.ta_user = User.objects.create(
            email_address='ta@example.com',
            password='password',
            first_name='TA',
            last_name='Assistant',
            home_address='123 TA St',
            phone_number='1234567893'
        )
        self.ta = TA.objects.create(user=self.ta_user, grader_status=False)
        self.ta_obj = TAObj(self.ta)

        # Create Instructor
        self.instructor_user = User.objects.create(
            email_address='instructor@example.com',
            password='password',
            first_name='Instructor',
            last_name='User',
            home_address='123 Instructor St',
            phone_number='1234567894'
        )
        self.instructor = Instructor.objects.create(user=self.instructor_user, max_assignments=1)
        self.instructor_obj = InstructorObj(self.instructor)

        # Add and remove instructor
        self.tempCourse.addInstructor(self.instructor_obj)
        self.tempCourse.removeAssignment(self.instructor_obj)

        # Add and remove TA
        self.tempCourse.addTa(self.ta_obj)
        self.tempCourse.removeAssignment(self.ta_obj)

    def test_remove_assignment(self):
        self.tempCourse.removeAssignment(self.ta_obj)
        # Check if the assignment (user) was removed from the course
        assignments = self.tempCourse.getAsgmtsForCrse()
        self.assertNotIn(self.ta_obj, assignments, "User was not removed from the course assignments")
        self.assertTrue(self.ta_obj not in assignments or assignments is None, "Tried to remove TA with no assignments")


class TestCourseRemoveCourse(TestCase):  #
    hold_course = None
    tempCourse = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=104,
            semester='Winter 2025',
            name='Basic Testing',
            description='Basic course on testing.',
            num_of_sections=1,
            modality='Remote'
        )
        self.tempCourse = CourseObj(self.hold_course)

    def test_remove_course(self):
        self.tempCourse.removeCourse()
        # Check if the course was removed
        course_exists = Course.objects.filter(id=self.hold_course.id).exists()
        self.assertFalse(course_exists, "Course was not removed")


class TestCourseEditCourseInfo(TestCase):  # Randall
    hold_course = None
    tempCourse = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=105,
            semester='Fall 2025',
            name='Testing Fundamentals',
            description='A course on testing fundamentals.',
            num_of_sections=4,
            modality='Mixed'
        )
        self.tempCourse = CourseObj(self.hold_course)
        self.new_info = {"semester": "Spring 2026", "name": "Advanced Testing Fundamentals", "description": "new",
                         "num_of_section": 3, "modality": "Online"}

    def test_edit_course_info(self):
        # Correct the key in new_info dictionary
        self.new_info = {"semester": "Spring 2026", "name": "Advanced Testing Fundamentals", "description": "new",
                         "num_of_sections": 3, "modality": "Online"}
        self.tempCourse.editCourse(self.new_info)
        self.hold_course.refresh_from_db()
        self.assertEqual(self.hold_course.semester, self.new_info["semester"], "Course semester was not updated")
        self.assertEqual(self.hold_course.name, self.new_info["name"], "Course name was not updated")
        self.assertEqual(self.hold_course.description, self.new_info["description"],
                         "Course description was not updated")
        self.assertEqual(self.hold_course.num_of_sections, self.new_info["num_of_sections"],
                         "Course section was not updated")
        self.assertEqual(self.hold_course.modality, self.new_info["modality"], "Course modality was not updated")

    def test_edit_course_incorrect_format(self):
        incorrect_info = {"semester": 2026, "num_of_sections": "invalid_number"}
        with self.assertRaises(ValidationError):
            self.tempCourse.editCourse(incorrect_info)

    def test_edit_course_with_incorrect_types(self):
        with self.assertRaises(ValidationError):  # Expect ValidationError, not TypeError
            self.tempCourse.editCourse({"num_of_sections": "three"})


class TestCourseGetAssignmentsForCourse(TestCase):  # Randall
    hold_course = None
    tempCourse = None
    user1 = None
    user2 = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        self.tempCourse = CourseObj(self.hold_course)
        # Example: Add some assignments to the course
        self.user1 = User.objects.create(
            email_address='user1@example.com',
            password='password1',
            first_name='Regular1',
            last_name='User1',
            home_address='123 User1 St',
            phone_number='1234567893'
        )
        self.user2 = User.objects.create(
            email_address='user2@example.com',
            password='password',
            first_name='Regular',
            last_name='User',
            home_address='123 User St',
            phone_number='1234567893'
        )
        # Create Instructor instances linked to User instances
        instructor1 = Instructor.objects.create(user=self.user1)
        instructor2 = Instructor.objects.create(user=self.user2)

        # Wrap these Instructor instances in InstructorObj and assign to self
        self.instructor_obj1 = InstructorObj(instructor1)
        self.instructor_obj2 = InstructorObj(instructor2)

        # Now add these InstructorObj instances to the course
        self.tempCourse.addInstructor(self.instructor_obj1)
        self.tempCourse.addInstructor(self.instructor_obj2)

    def test_get_assignments_for_course(self):
        assignments = self.tempCourse.getAsgmtsForCrse()
        # Find the InstructorToCourse objects for instructor1 and instructor2
        instructor1_assignment = InstructorToCourse.objects.get(instructor=self.instructor_obj1.database)
        instructor2_assignment = InstructorToCourse.objects.get(instructor=self.instructor_obj2.database)

        # Assertions to verify the correct assignments are returned
        self.assertIn(instructor1_assignment, assignments['instructors'],
                      "Instructor1 is not in the course assignments")
        self.assertIn(instructor2_assignment, assignments['instructors'],
                      "Instructor2 is not in the course assignments")

    def test_no_assignments(self):
        new_course = Course.objects.create(
            course_id=102,
            semester='Spring 2024',
            name='No Assignment Course',
            description='A course with no assignments.',
            num_of_sections=2,
            modality='Remote'
        )
        new_temp_course = CourseObj(new_course)

        # Now get assignments for this new course
        assignments = new_temp_course.getAsgmtsForCrse()

        # Assert that there are no instructors or tas
        self.assertEqual(assignments['instructors'], [], "There should be no instructors assigned")
        self.assertEqual(assignments['tas'], [], "There should be no TAs assigned")


class TestCourseGetSectionsForCourse(TestCase):  # Randall
    hold_course = None
    tempCourse = None
    section1 = None
    section2 = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=102,
            semester='Spring 2024',
            name='Advanced Testing',
            description='A course about advanced testing methods.',
            num_of_sections=2,
            modality='Hybrid'
        )
        self.tempCourse = CourseObj(self.hold_course)
        self.section1 = Section.objects.create(
            section_id=201,
            course=self.hold_course,
            meeting_time='2024-01-15 09:00:00'  # Example datetime format
        )
        self.section2 = Section.objects.create(
            section_id=202,
            course=self.hold_course,
            meeting_time='2024-01-15 11:00:00'  # Example datetime format
        )

    def test_get_sections_for_course(self):
        sections = self.tempCourse.getSectionsCrse()
        self.assertIn(self.section1, sections, "Section1 is not in the course sections")
        self.assertIn(self.section2, sections, "Section2 is not in the course sections")

    def test_no_sections(self):
        # Remove sections before testing
        Section.objects.all().delete()
        sections = self.tempCourse.getSectionsCrse()
        self.assertEqual(sections, [])


class TestCourseGetCourseInfo(TestCase):  # Randall
    hold_course = None
    tempCourse = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=103,
            semester='Winter 2025',
            name='Basic Testing',
            description='Basic course on testing.',
            num_of_sections=1,
            modality='Remote'
        )
        self.tempCourse = CourseObj(self.hold_course)

    def test_get_course_info(self):
        info = self.tempCourse.getCrseInfo()
        # Assertions to verify the correct course info is returned
        self.assertEqual(info['course_id'], self.hold_course.course_id, "Course ID is incorrect")
        self.assertEqual(info['name'], self.hold_course.name, "Course name is incorrect")
        self.assertEqual(info['description'], self.hold_course.description, "Course description is incorrect")
        self.assertEqual(info['num_of_sections'], self.hold_course.num_of_sections, "Course section is incorrect")
        self.assertEqual(info['modality'], self.hold_course.modality, "Course modality is incorrect")


class TestSectionGetID(TestCase):  # Joe
    lab = None
    course = None

    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        self.course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        self.lab = LabObj(Lab(section=tmp_section))

    def test_get_id(self):
        self.assertEqual(self.lab.getID(), 1011, "getID() did not retrieve correct section_id")


class TestSectionGetParentCourse(TestCase):  # Joe
    lab = None
    course = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        self.course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )

        tmp_lab = Lab.objects.create(
            section=tmp_section,
            ta=tmp_ta
        )

        self.lab = LabObj(tmp_lab)

    def test_get_parent_course(self):
        self.assertEqual(self.lab.getParentCourse(), self.course,
                         "getParentCourse() did not retrieve correct course")


class TestLabInit(TestCase):
    lab = None
    info = None
    tempLab = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        self.tmp_lab = Lab.objects.create(
            section=tmp_section,
            ta=tmp_ta
        )

        self.lab = LabObj(self.tmp_lab)

    def test_lab_make(self):
        self.assertIsNotNone(self.lab, "__init__ failed in making Lab")

    def test_bad_lab_make(self):
        with self.assertRaises(TypeError, msg="__init__ failed in making Lab, bad input"):
            LabObj(5)


class TestLabGetLabTAAssignment(TestCase):  # Joe
    lab = None
    ta = None

    # noinspection DuplicatedCode
    def setUp(self):
        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )

        self.lab = Lab.objects.create(
            section=tmp_section
        )

    def test_get_ta(self):
        temp = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp.save()
        self.ta = TA.objects.create(user=temp, grader_status=True)
        self.ta.save()

        self.lab.ta = self.ta
        self.lab.save()

        self.labObj = LabObj(self.lab)  # Form lab after adding TA manually

        self.assertEqual(
            self.ta,
            self.labObj.getLabTAAsgmt(),
            "getLabTAAssignment() does not retrieve correct ta; Test may also be accepting wrong object")

    def test_get_but_no_ta(self):
        self.labObj = LabObj(self.lab)  # Form lab with no TA

        self.assertIsNone(self.labObj.getLabTAAsgmt(), "getLabTAAssignment() finds something with no TA")


class TestLabAddTA(TestCase):  # Joe
    lab = None
    ta = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        self.ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        self.ta.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lab = Lab.objects.create(
            section=tmp_section,
        )
        tmp_lab.save()

        self.lab = LabObj(tmp_lab)

    def test_add_ta(self):
        self.lab.addTA(self.ta)
        # Gives error for TAObj having no 'user' but I think that's because __init__ not implemented in my branch
        self.assertEqual(self.ta, self.lab.getLabTAAsgmt(),
                         "addTA() does not add TA to lab")

    def test_add_ta_but_full(self):
        temp2 = User(email_address="test2@test.com", password="password2", first_name="first2", last_name="last2",
                     home_address="Your mom's house", phone_number=1234567890)
        temp2.save()
        temp_ta = TA.objects.create(user=temp2, grader_status=True)
        self.lab.addTA(self.ta)
        # Gives error for TAObj having no 'user' but I think that's because __init__ not implemented in my branch
        with self.assertRaises(RuntimeError, msg="Tried to add TA to full Lab"):
            self.lab.addTA(temp_ta)


class TestLabRemoveTA(TestCase):  # Joe
    lab = None
    ta = None

    def setUp(self):
        temp_user = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lab = Lab.objects.create(
            section=tmp_section,
            ta=tmp_ta
        )

        self.lab = LabObj(tmp_lab)

    def test_remove(self):
        self.lab.removeTA()
        self.assertIsNone(self.lab.getLabTAAsgmt(), "removeTA() does not remove TA from lab")

    def test_none_to_remove(self):
        self.lab.removeTA()
        with self.assertRaises(RuntimeError, msg="Tried to remove TA when none in lab"):
            self.lab.removeTA()


class TestLectureInit(TestCase):
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        self.lecture = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta,
            instructor=tmp_instructor
        )
        self.lecture.save()

    def test_lecture_make(self):
        self.assertIsNotNone(LectureObj(self.lecture), "__init__ failed in making Lecture")

    def test_bad_lecture_make(self):
        with self.assertRaises(TypeError, msg="__init__ failed in making Lecture: Type error"):
            self.lecture = LectureObj(7)


class TestLectureGetLecInstrAssignment(TestCase):  # Joe
    instructor = None
    lecture = None

    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta
        )
        tmp_lec.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        self.instructor = Instructor.objects.create(
            user=temp_user2
        )
        self.instructor.save()

        self.lecture = LectureObj(tmp_lec)

    def test_get_instructor(self):
        self.lecture.addInstr(self.instructor)
        self.assertEqual(self.instructor, self.lecture.getLecInstrAsmgt(),
                         "getLecInstrAssignment() does not return correct")

    def test_get_with_no_instructor(self):
        self.assertIsNone(self.lecture.getLecInstrAsmgt(),
                          "getLecInstrAssignment() Retrieved instructor when none exists")


class TestLectureAddInstructor(TestCase):  # Joe
    lecture = None
    instructor = None

    def setUp(self):
        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        self.instructor = Instructor.objects.create(
            user=temp_user2
        )
        self.instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section
        )
        tmp_lec.save()

        self.info = {
            "section", tmp_section,
        }

        self.lecture = LectureObj(tmp_lec)

    def test_add_but_full(self):
        self.lecture.addInstr(self.instructor)
        with self.assertRaises(RuntimeError, msg="Tried to add Instructor to full lecture"):
            self.lecture.addInstr(self.instructor)

    def test_add(self):
        self.lecture.addInstr(self.instructor)
        self.assertEqual(
            self.lecture.getLecInstrAsmgt(),
            self.instructor,
            "getLecInstrAssignment() Did not add instructor to lecture"
        )


# noinspection DuplicatedCode
class TestLectureRemoveInstructor(TestCase):  # Joe
    instructor = None
    lecture = None

    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta,
            instructor=tmp_instructor
        )
        tmp_lec.save()

        self.lecture = LectureObj(tmp_lec)

    def test_none_to_remove(self):
        self.lecture.removeInstr()
        with self.assertRaises(RuntimeError, msg="removeInstr() Tried to remove from lecture with no instructor"):
            self.lecture.removeInstr()

    def test_remove(self):
        self.lecture.removeInstr()
        self.assertIsNone(self.lecture.getLecInstrAsmgt(), "removeInstr() did not remove from lecture")


class TestLectureGetLecTAAssignment(TestCase):  # Joe
    ta = None
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        self.ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        self.ta.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=self.ta,
            instructor=tmp_instructor
        )
        tmp_lec.save()

        self.lecture = LectureObj(tmp_lec)

    def test_get_ta_assignment(self):
        self.assertEqual(
            self.lecture.getLectureTAAsgmt(),
            self.ta,
            "getLectureTAAssignment() Retrieved incorrect TA from lecture"
        )

    def test_get_no_ta_assignment(self):
        self.lecture.removeTA()
        self.assertIsNone(
            self.lecture.getLectureTAAsgmt(),
            "getLectureTAAssignment() retrieved a TA from lecture when none exists"
        )


class TestLectureAddTA(TestCase):  # Joe
    ta = None
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()
        self.ta = tmp_ta

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            instructor=tmp_instructor
        )
        tmp_lec.save()

        self.lecture = LectureObj(tmp_lec)

    def test_add(self):
        self.lecture.addTA(self.ta)
        self.assertEqual(self.lecture.getLectureTAAsgmt(), self.ta, "addTA() did not add correct TA to lecture")

    def test_add_but_full(self):
        self.lecture.addTA(self.ta)
        with self.assertRaises(RuntimeError, msg="addTA() Tried to add to full lecture"):
            self.lecture.addTA(self.ta)


class TestLectureRemoveTA(TestCase):  # Joe
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta,
            instructor=tmp_instructor
        )
        tmp_lec.save()

        self.info = {
            "ta", tmp_ta,
            "section", tmp_section,
            "instructor", tmp_instructor
        }

        self.lecture = LectureObj(tmp_lec)

    def test_none_to_remove(self):
        self.lecture.removeTA()
        with self.assertRaises(RuntimeError, msg="removeTA() Tried to remove from none from lecture"):
            self.lecture.removeTA()

    def test_remove(self):
        self.lecture.removeTA()
        self.assertIsNone(self.lecture.getLectureTAAsgmt(), "removeTA() did not remove from lecture")


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


class GetAllUserAssignmentsTest(TestCase):
    def setUp(self):
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

        # Assign instructor to course
        InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)

        # Creating user and TA object
        self.user = User.objects.create(email_address="ta@example.com", password="password123",
                                        first_name="TAFirstName", last_name="TALastName", home_address="TA Address",
                                        phone_number=1234567890)
        self.ta = TA.objects.create(user=self.user, grader_status=True, max_assignments=3)

        # Assign TA to course
        TAToCourse.objects.create(ta=self.ta, course=self.course)

    def test_get_ta_assignments(self):
        instructor_obj = InstructorObj(self.instructor)

        # Fetch the assignments using the method
        assignments = instructor_obj.getInstrCrseAsgmts()

        # Convert assignments to a format that can be compared
        formatted_assignments = []
        for assignment in assignments:
            course_id = assignment.course.id
            instructor_id = assignment.instructor.id

            # Get TAs for each course and check if they match the expected TA
            tas_for_course = TAToCourse.objects.filter(course__id=course_id)
            for ta_assignment in tas_for_course:
                if ta_assignment.ta.id == self.ta.id:
                    # Get sections associated with the course
                    sections = Section.objects.filter(course__id=course_id)
                    for section in sections:
                        formatted_assignments.append({
                            "taID": ta_assignment.ta.id,
                            "secID": section.id,
                            "courseID": course_id
                        })

        # Check the content of the assignments list
        expected_assignment = {
            "taID": self.ta.id,
            "secID": self.section.id,
            "courseID": self.course.id
        }
        self.assertIn(expected_assignment, formatted_assignments, "TA assignment not found in instructor assignments")

    def test_ta_assigned_to_another_course(self):
        # Create a new course and TA
        other_course = Course.objects.create(course_id=124, semester="Spring", name="Other Course",
                                             description="Another course", num_of_sections=1, modality="In-Person")
        other_ta_user = User.objects.create(email_address="other_ta@example.com", password="other_password",
                                            first_name="OtherTA", last_name="User", home_address="Other Address",
                                            phone_number=987654321)
        other_ta = TA.objects.create(user=other_ta_user, grader_status=True, max_assignments=3)

        # Assigning the new TA to the other course
        TAToCourse.objects.create(ta=other_ta, course=other_course)

        instructor_obj = InstructorObj(self.instructor)

        assignments = instructor_obj.getInstrCrseAsgmts()

        # Checking that the other TA is not in the assignments list
        unexpected_assignment = {
            "taID": other_ta.id,
            "secID": self.section.id,
            "courseID": other_course.id
        }
        self.assertNotIn(unexpected_assignment, assignments, "TA from another course found in instructor assignments")
