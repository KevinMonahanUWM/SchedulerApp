import datetime

from django.test import TestCase
from TAScheduler.models import Course, User, TA, Section, Lab, Administrator, InstructorToCourse, TAToCourse, \
    Instructor, Lecture
from TAScheduler.views_methods import CourseObj, AdminObj, TAObj, LabObj, InstructorObj, LectureObj
from django.core.exceptions import ValidationError


# SEE METHOD DESCRIPTIONS FOR GUIDE ON HOW TO WRITE.
# Feel free to make suggestions on discord (add/remove/edit methods)!.
# Remember: These methods were made before any coding (I was guessing) so it's likely they should be changed.

class TestUserLogin(TestCase):  # Alec
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
        result = self.adminObj.login("test@example.com", "password123")
        self.assertRedirects(result, '/home/', msg_prefix="login with valid credentials failed to redirect to home")

    def test_login_invalid_credentials(self):
        result = self.adminObj.login("test@example.com", "wrong_password")
        self.assertRedirects(result, '/', msg_prefix="incorrect password failed to redirect to login")


class TestUserGetID(TestCase):  # Alec
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
        self.assertEqual(user_id, "test@example.com", msg="user.getUsername failed to return username")


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
        self.assertEqual(self.adminObj.getPassword(), "password123", msg="user.getPassword failed to retrieve password")


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
        self.assertEqual(self.adminObj.getName(), "Test User", msg="user.getName failed to retrieve name")


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
        self.assertEqual(self.adminObj.getRole(), "admin", msg="user.getRole failed to retrieve 'admin'")


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
        course_info = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Intro to Testing',
            description='A course about unit testing',
            num_of_sections=3,
            modality='Online',
            credits=4
        )
        self.courseObj = CourseObj(course_info)

    def test_create_course(self):
        created_course = self.adminObj.createCourse(self.courseObj)
        self.assertIsNotNone(created_course)
        self.assertEqual(created_course.name, 'Intro to Testing', msg="failed to create course")


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
            "email_address": 'newuser@example.com',
            "password": 'password123',
            "first_name": 'New',
            "last_name": 'User',
            "home_address": '123 New Street',
            "phone_number": 9876543210,
            "role": "TA"
        }
        created_user = self.adminObj.createUser(user_info)
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email_address, 'newuser@example.com', msg="user not created")


class TestAdminCreateSection(TestCase):  # Alec
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

        self.course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Intro to Django Testing',
            description='A comprehensive course on testing in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )
        self.section = Section.objects.create(
            section_id=201,
            course=self.course,
            location='Room 101',
            meeting_time=datetime.datetime.now()
        )

    def test_create_section(self):
        created_section = self.adminObj.createSection(self.section)
        self.assertIsNotNone(created_section)
        self.assertEqual(created_section.section_id, 201, msg="failed to create section")


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
            credits=4
        )
        self.tempCourse = CourseObj(self.hold_course)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
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
            phone_number='1234667890'
        )
        temp_ta = TA.objects.create(user=self.hold_user, grader_status=False)
        self.tempTA = TAObj(temp_ta)
        temp = User.objects.create(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
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
            modality='Online',
            credits=4
        )
        self.hold_sec = Section.objects.create(
            section_id=1011,
            course=temp_course,
            location="A distant realm",
            meeting_time=datetime.datetime
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
            phone_number='1234567890'
        )
        hold_admin = Administrator(user=temp)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

    def test_successful_delete(self):
        self.admin.removeSection(self.tempLab)
        self.assertNotIn(User.objects, self.hold_sec, "Did not remove section from the database")

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
            modality='Online',
            credits=4
        )
        self.tempCourse = CourseObj(hold_course)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.new_info = {"course id": 103,
                         "semester": "Spring 2024",
                         "name": "Intro to Units",
                         "description": "Unit testing at its finest",
                         "num of sections": 4,
                         "modality": "",
                         "credits": 3}

    def test_bad_course(self):
        with self.assertRaises(TypeError, msg='Course that was passed is not a valid course'):
            self.admin.editCourse(11, self.new_info)

    def test_bad_info(self):
        with self.assertRaises(TypeError, msg='Improper input entered for editing course'):
            self.admin.editCourse(self.tempCourse, 11)

    def test_success(self):
        self.admin.editCourse(self.tempCourse, self.new_info)
        self.assertEqual(self.new_info["description"], Course.objects.get(course_id=103))

    def test_bad_item_in_info(self):
        info = {"course id", 103,
                "semester", "Spring 2024",
                "name", 4,
                "description", "Unit testing at its finest",
                "num of sections", "4",
                "modality", "",
                "credits", "3 or so"}
        with self.assertRaises(TypeError, msg='Improper input entered for editing course'):
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
            modality='Online',
            credits=4
        )
        hold_sec = Section.objects.create(
            section_id=1011,
            course=hold_course,
            location="The end of the universe",
            meeting_time=datetime.datetime
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
            phone_number='1234567890'
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.new_info = {"section id": 1012,
                         "location": "Somewhere in the universe",
                         "meeting time": datetime.datetime}

    def test_bad_section(self):
        with self.assertRaises(TypeError, msg='Section that was passed is not a valid section'):
            self.admin.editSection(11, self.new_info)

    def test_bad_info(self):
        with self.assertRaises(TypeError, msg='Improper input entered for editing section'):
            self.admin.editSection(self.tempLab, 11)

    def test_success(self):
        self.admin.editSection(self.tempLab, self.new_info)
        self.assertEqual(self.new_info["location"], Section.objects.get(section_id=1012).location)


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
            phone_number='1234667890'
        )
        temp_ta = TA.objects.create(user=self.hold_user, grader_status=False)
        self.tempTA = TAObj(temp_ta)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.new_info = {"grader status": True,
                         "max assignments": 3,
                         "first name": "Paul",
                         "last name": "Different"}

    def test_bad_course(self):
        with self.assertRaises(TypeError, msg='User that was passed is not a valid user'):
            self.admin.editUser(11, self.new_info)

    def test_bad_info(self):
        with self.assertRaises(TypeError, msg='Improper input entered for editing user'):
            self.admin.editUser(self.tempTA, 11)

    def test_success(self):
        self.admin.editUser(self.tempTA, self.new_info)
        self.assertEqual(self.new_info["first name"], Section.objects.get(section_id=1012))


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
            modality='Online',
            credits=4
        )
        self.tempCourse = CourseObj(self.hold_course)
        self.hold_user = User.objects.create(
            email_address='kev@example.com',
            password='kev_password',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number='1234667890'
        )
        self.hold_instr = Instructor.objects.create(user=self.hold_user)
        self.tempInstr = InstructorObj(self.hold_instr)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
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
        temp = User.objects.create(self.hold_user)
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
            modality='Online',
            credits=4
        )
        self.tempCourse = CourseObj(self.hold_course)
        self.hold_user = User.objects.create(
            email_address='kev@example.com',
            password='kev_password',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number='1234667890'
        )
        self.hold_ta = TA.objects.create(user=self.hold_user, grader_status=True)
        self.tempTA = TAObj(self.hold_ta)
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
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
        temp = User.objects.create(self.hold_user)
        ta = TA.objects.create(
            user=temp,
            max_assignments=0,
            grader_status=False
        )
        temp_ta = TAObj(ta)
        with self.assertRaises(RuntimeError, msg="Tried to link course to TA with max assignments"):
            self.admin.courseTAAsmgt(temp_ta, self.tempCourse)


class TestTAInit(TestCase):
    ta_database = None
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
        self.ta_database = TA.objects.create(user=self.user, grader_status=False)

    def test_bad_input(self):
        with self.assertRaises(TypeError, msg='TA that was passed is not a valid TA'):
            TAObj(11)

    def test_null_ta(self):
        User.delete(self.user)
        with self.assertRaises(TypeError, msg='TA that was passed does not exist'):
            TAObj(self.ta_database)

    def test_success(self):
        ta = TAObj(self.ta_database)
        self.assertEqual(ta.database, self.ta_database,
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
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database.
        temp_user_for_admin = User(email_address='admin@example.com',
                                   password='admin_password',
                                   first_name='Admin',
                                   last_name='User',
                                   home_address='123 Admin St',
                                   phone_number='1234567890')
        temp_admin = Administrator(user=temp_user_for_admin)
        self.adminObj = AdminObj(temp_admin)

        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )

    # 1] TA w/ 1 course assignment
    def test_1Course1MaxCap(self):
        TAToCourse.objects.create(ta=self.taDB, course=self.courseDB)  # assigning TA to course using db?
        self.assertEquals(self.taObj.hasMaxAsgmts(), True,
                          msg="TA has 1 max assignments & assigned 1 course: @ max cap")

    # [2] TA w/ 0 course assignment
    def test_0Course1MaxCap(self):
        self.assertEquals(self.taObj.hasMaxAsgmts(), False,
                          msg="TA has 1 max assignments & not assigned 1 course: not @ max cap")

    # [3] TA w/ max cap -> no max assign
    # using views method: I know bad practice but this is still a good test to ensure both method's working correctly
    def test_origMaxCapToNoAssignment(self):
        TAToCourse.objects.create(ta=self.taDB, course=self.courseDB)
        self.adminObj.removeCourse(CourseObj(self.courseDB))
        self.assertEquals(self.taObj.hasMaxAsgmts(), False,
                          msg="TA originally w/ assignment, removed, shouldn't be at max cap")


class TestTAAssignTACourse(TestCase):  # Kiran
    taDB = None
    courseDBList = list()
    courseList = list()
    user = None  # for TA
    taObj = None

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=2)  # max 2 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database

        for i in [1, 2, 3]:
            self.courseDBList.append(Course.objects.create(
                course_id=100 + i,
                semester='Fall 2023',
                name='Introduction to Testing',
                description='A course about writing tests in Django.',
                num_of_sections=3,
                modality='Online',
                credits=4
            ))
            self.courseList.append(Course(self.courseDBList[i]))  # ADDED FROM REVIEW!

    # [1] Success TA->Course
    def test_ExistCourse(self):
        self.taObj.assignTACourse(self.courseList[0])
        self.assertIn(self.courseDBList[0], TAToCourse.objects.filter(course=self.courseDBList[0], ta=self.taDB).course,
                      "Should have linked course and TA together")

    # [2] Adding Course not existing in DB
    def test_NotExistCourse(self):
        temp_course = CourseObj(Course(course_id=104, semester='Fall 2023',
                                       name='Introduction to Testing',
                                       description='A course about writing tests in Django.',
                                       num_of_sections=3,
                                       modality='Online',
                                       credits=4))  # id =104, not 101,102,103
        with self.assertRaises(ValueError, msg="can't send in non existing course, i.e., course obj"):
            self.taObj.assignTACourse(temp_course)

    # [3] Adding duplicate course
    def test_duplicateCourse(self):
        self.taObj.assignTACourse(self.courseList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a TA the same course twice"):
            self.taObj.assignTACourse(self.courseList[0])

    # [4] Adding Course to TA @ max capacity
    def test_OverCap(self):
        self.taObj.assignTACourse(self.courseList[0])
        self.taObj.assignTACourse(self.courseList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max TA assignments"):
            self.taObj.assignTACourse(self.courseList[2])

    # [5] Trying to add a non-course
    def test_NonCourse(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(TypeError, msg="Shouldn't be allowed to assign TA to non-course"):
                    self.taObj.assignTACourse(invalid_input)


class TestTAGetTACourseAssignments(TestCase):  # Kiran
    taDB = None
    courseDB = None
    course = None
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
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database.
        temp_user_for_admin = User(email_address="admin@example.com")
        temp_admin = Administrator(user=temp_user_for_admin)
        self.adminObj = AdminObj(temp_admin)

        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )
        self.course = CourseObj(self.courseDB)

    # [1] 1 assignment
    def test_1Assignment(self):
        self.taObj.assignTACourse(self.course)
        self.assertEquals(self.taObj.getTACrseAsgmts(), 1, msg="should be 1 assigment")

    # [2] 0 assignment
    def test_0Assignment(self):
        self.assertEquals(self.taObj.getTACrseAsgmts(), 0, msg="should be 0 assignments")

    # [3] 1->0 Assignment
    # using views method: same reasons above^
    def test_1to0Assignment(self):
        self.taObj.assignTACourse(self.course)
        self.adminObj.removeCourse(self.course)
        self.assertEquals(self.taObj.getTACrseAsgmts(), 0, msg="added then removed course, should be 0")


class TestAssignTALab(TestCase):
    taDB = None
    courseDBList = list()  # just for section
    sectionDBList = list()  # just for lab
    labDBList = list()
    labList = list()
    user = None  # for TA
    taObj = None

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=3)  # max 2 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database

        for i in [1, 2, 3]:  # courses
            self.courseDBList.append(Course.objects.create(
                course_id=100 + i,
                semester='Fall 2023',
                name='Introduction to Testing',
                description='A course about writing tests in Django.',
                num_of_sections=3,
                modality='Online',
                credits=4
            ))
        for i in [1, 2, 3]:  # section
            self.sectionDBList.append(Section.objects.create(
                section_id=100 + i,
                course=self.courseDBList[i],
                location="location" + str(i),
                meeting_time="mt" + str(i)
            ))
        for i in [1, 2, 3]:  # lab
            self.labDBList.append(Lab.objects.create(
                section_id=self.sectionDBList[i],
                ta=None  # HOPEFULLY FINE?
            ))
            self.labList.append(LabObj(self.labDBList[i]))

    # [1] Success TA->Lab
    def test_ExistLab(self):
        self.taObj.assignTALab(self.labList[0])
        self.assertIn(self.taObj.database, Lab.objects.get(ta=self.taDB).ta,
                      "Should have linked lab and TA together")

    # [2] Adding Lab not existing in DB
    def test_NotExistLab(self):
        temp_lab = LabObj(Lab(section=self.sectionDBList[0]))  # created, not saved to db
        with self.assertRaises(ValueError, msg="can't send in non existing lab, i.e., lab obj"):
            self.taObj.assignTALab(temp_lab)

    # [3] Adding duplicate lab: (don't know why this would happen but might as well test it :P)
    def test_duplicateLab(self):
        self.taObj.assignTALab(self.labList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a TA the same lab twice"):
            self.taObj.assignTALab(self.labList[0])

    # [4] Adding TA to Lab @ max cap
    def test_OverCap(self):
        self.taObj.assignTALab(self.labList[0])
        self.taObj.assignTALab(self.labList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max TA assignments"):
            self.taObj.assignTALab(self.labList[2])

    # [5] Trying to add a non-lab
    def test_NonLab(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(ValueError, msg="Shouldn't be allowed to assign TA to non-course"):
                    self.taObj.assignTALab(invalid_input)

    # [6] Assigning lab TA w/ grader status
    def test_GraderStatus(self):
        temp_user = User.objects.create(email_address='grader@gmail.com', password='TA_password',
                                        first_name='TA',
                                        last_name='User',
                                        home_address='123 TA St',
                                        phone_number='1234567890')  # HOPEFULLY DON'T NEED ALL FIELDS?
        temp_ta = TA.objects.create(user=temp_user, max_assignments=2,
                                    grader_status=True)  # new TA in db W/ GraderStatus
        self.taObj = TAObj(temp_ta)
        with self.assertRaises(RuntimeError, msg="TA can't assign to lab when grader"):
            self.taObj.assignTALab(self.labList[0])


class TestTAGetTALabAssignments(TestCase):  # Kiran
    taDB = None
    labDB = None
    lab = None
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
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.taObj = TAObj(self.taDB)
        temp_user_for_admin = User(email_address="admin@example.com")  # HOPEFULLY OK W/O FIELDS?
        temp_admin = Administrator(user=temp_user_for_admin)
        self.adminObj = AdminObj(temp_admin)

        # Course
        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4)
        # Section
        self.sectionDB = Section.objects.create(
            section_id=100 + 1,
            course=self.courseDB,
            location="location" + str(1),
            meeting_time="mt" + str(1))
        # Lab - create assignments in the test.

    # [1] 1 lab assignment
    def test_1Assignment(self):
        Lab.objects.create(section_id=self.sectionDB, ta=self.taObj)  # creating assignment?
        self.assertEquals(self.taObj.getTALabAsgmts(), 1, msg="should be 1 assigment")

    # [2] 0 lab assignment
    def test_0Assignment(self):
        self.assertEquals(self.taObj.getTALabAsgmts(), 0, msg="should be 0 assignments")

    # [3] 1 lab "assignment" - not in db
    def test_1AssignmentNoExistLab(self):
        temp_section = Section(section_id=102,
                               course_id=self.courseDB)  # not "101", which exists already HOPEFULLY OK W/O ALL FIELDS?
        Lab(section=temp_section, ta=self.taObj)
        self.assertEquals(self.taObj.getTALabAsgmts(), 0, msg="shouldn't assign non-existing lab")

    # [4] 1->0 lab Assignment
    # Using views method: I know not good practice but this is still a good check for both of the assign/remove methods.
    def test_1to0Assignment(self):
        self.taObj.assignTALab(self.labDB)
        self.adminObj.removeSection(self.labDB)
        self.assertEquals(self.taObj.getTALabAsgmts(), 0, msg="added then removed lab, should be 0")


class TestAssignTALec(TestCase):  # Kiran
    taDB = None
    courseDBList = list()  # just for section
    sectionDBList = list()  # just for lec
    lecDBList = list()
    lecList = list()
    user = None  # for TA
    taObj = None

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=2)  # max 2 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database

        for i in [1, 2, 3]:  # courses
            self.courseDBList.append(Course.objects.create(
                course_id=100 + i,
                semester='Fall 2023',
                name='Introduction to Testing',
                description='A course about writing tests in Django.',
                num_of_sections=3,
                modality='Online',
                credits=4
            ))
        for i in [1, 2, 3]:  # section
            self.sectionDBList.append(Section.objects.create(
                section_id=100 + i,
                course=self.courseDBList[i],
                location="location" + str(i),
                meeting_time="mt" + str(i)
            ))
        for i in [1, 2, 3]:  # lec
            self.lecDBList.append(
                Lecture.objects.create(section_id=self.sectionDBList[i]))  # HOPEFULLY FINE W/O FIELDS?
            self.lecList.append(LectureObj(self.lecDBList[i]))

    # [1] Success TA->Lec
    def test_ExistLLec(self):
        self.taObj.assignTALecture(self.lecList[0])
        self.assertIn(self.taObj.database, Lecture.objects.get(ta=self.taDB).ta,
                      "Should have linked lec and TA together")

    # [2] Adding Lec not existing in DB
    def test_NotExistLec(self):
        temp_lec = LectureObj(Lecture(section=self.sectionDBList[0]))  # created, not saved to db
        with self.assertRaises(ValueError, msg="can't send in non existing lecture, i.e., lecture obj"):
            self.taObj.assignTALecture(temp_lec)

    # [3] Adding duplicate lec: (don't know why this would happen but might as well test it :P)
    def test_duplicateLec(self):
        self.taObj.assignTALecture(self.lecList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a TA the same lec twice"):
            self.taObj.assignTALecture(self.lecList[0])

    # [4] Adding TA to Lab @ max cap
    def test_OverCap(self):
        self.taObj.assignTALecture(self.lecList[0])
        self.taObj.assignTALecture(self.lecList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max TA assignments"):
            self.taObj.assignTALecture(self.lecList[2])

    # [5] Trying to add a non-lec.
    def test_NonLab(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types
        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(ValueError, msg="Shouldn't be allowed to assign TA to non-course"):
                    self.taObj.assignTALecture(invalid_input)

    # [6] Assigning lec TA w/o grader status
    def test_GraderStatus(self):
        temp_user = User.objects.create(email_address='grader@gmail.com')  # HOPEFULLY DON'T NEED ALL FIELDS?
        temp_ta = TA.objects.create(user=temp_user, max_assignments=2, grader_status=False)  # w/o GraderStatus
        self.taObj = TAObj(temp_ta)  # reassigning
        with self.assertRaises(ValueError, msg="TA can't assign to lec when grader"):
            self.taObj.assignTALecture(self.lecList[0])


class TestTAGetTALecAssignments(TestCase):  # Kiran
    taDB = None
    lecDB = None
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
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=1, grader_status=True)  # gs=T, max 1 assignment!
        self.taObj = TAObj(self.taDB)
        temp_user_for_admin = User(email_address="admin@example.com")  # HOPEFULLY OK W/O FIELDS?
        temp_admin = Administrator(user=temp_user_for_admin)
        self.adminObj = AdminObj(temp_admin)

        # Course
        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4)
        # Section
        self.sectionDB = Section.objects.create(
            section_id=100 + 1,
            course=self.courseDB,
            location="location" + str(1),
            meeting_time="mt" + str(1))
        # Lecture - create assignments in the test.

    # [1] 1 lecture assignment
    def test_1Assignment(self):
        Lecture.objects.create(section_id=self.sectionDB, ta=self.taDB)  # creating assignment?
        self.assertEquals(self.taObj.getTALecAsgmts(), 1, msg="should be 1 assigment")

    # [2] 0 lab assignment
    def test_0Assignment(self):
        self.assertEquals(self.taObj.getTALabAsgmts(), 0, msg="should be 0 assignments")

    # [3] 1 lab "assignment" - not in db
    def test_1AssignmentNoExistLab(self):
        temp_section = Section(section_id=102)  # not "101", which exists already HOPEFULLY OK W/O ALL FIELDS?
        temp_lec = LectureObj(Lecture(section=temp_section))
        self.taObj.assignTALecture(temp_lec)
        self.assertEquals(self.taObj.getTALecAsgmts(), 0, msg="shouldn't assign non-existing lecture")

    # [4] 1->0 lab Assignment
    # Using views method: I know not good practice but this is still a good check for both of the assign/remove methods.
    def test_1to0Assignment(self):
        self.taObj.assignTALecture(self.lecDB)
        self.adminObj.removeSection(self.lecDB)
        self.assertEquals(self.taObj.getTALecAsgmts(), 0, msg="added then removed lecture, should be 0")


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
                phone_number='1234567890')
            )
        self.taDB1 = TA.objects.create(user=self.userDBList[0], max_assignments=1, grader_status=True)
        self.taDB2 = TA.objects.create(user=self.userDBList[1], max_assignments=1, grader_status=False)
        self.taObj1 = TAObj(self.taDB1)  # grader
        self.taObj2 = TAObj(self.taDB2)  # non-grader

    # [1] Getting non-grader status
    def test_nonGraderStatus(self):
        self.assertEquals(self.taObj1.getGraderStatus(), True, msg="grader status ta should have true GS field")

    # [2] Getting grader status
    def test_graderStatus(self):
        self.assertEquals(self.taObj2.getGraderStatus(), False, msg="non grader status ta should have false GS field")


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
        self.instructorDB = Instructor.objects.create(user=self.user)

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
            phone_number='1234567890'
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.instrObj = InstructorObj(self.instrDB)
        temp_user_for_admin = User(email_address="admin@example.com")
        temp_admin = Administrator(user=temp_user_for_admin)
        self.adminObj = AdminObj(temp_admin)

        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )

    # [1] Instr w/ 1 course assignment
    def test_1Course1MaxCap(self):
        InstructorToCourse.objects.create(instructor=self.instrDB, course=self.courseDB)
        self.assertEquals(self.instrObj.hasMaxAsgmts(), True,
                          msg="instructor has 1 max assignments & assigned 1 course: @ max cap")

    # [2] Instr w/ 0 course assignment
    def test_0Course1MaxCap(self):
        self.assertEquals(self.instrObj.hasMaxAsgmts(), False,
                          msg="instructor has 1 max assignments & not assigned 1 course: not @ max cap")

    # [3] Instr w/ max cap -> no max assign
    # using views method
    def test_origMaxCapToNoAssignment(self):
        InstructorToCourse.objects.create(instructor=self.instrDB, course=self.courseDB)
        self.adminObj.removeCourse(
            CourseObj(self.courseDB))  # removing course SHOULD also remove this instructor's assignment
        self.assertEquals(self.instrObj.hasMaxAsgmts(), False,
                          msg="instructor originally w/ assignment, removed, shouldn't be at max cap")


class TestInstructorAssignInstrCourse(TestCase):  # Kiran
    instrDB = None
    courseDBList = list()
    courseList = list()
    user = None  # for TA
    instrObj = None

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=2)  # max 2 assignment!
        self.instrObj = InstructorObj(self.instrDB)  # creating TA object using TA in database

        for i in [1, 2, 3]:
            self.courseDBList.append(Course.objects.create(
                course_id=100 + i,
                semester='Fall 2023',
                name='Introduction to Testing',
                description='A course about writing tests in Django.',
                num_of_sections=3,
                modality='Online',
                credits=4
            ))
            self.courseList.append(CourseObj(self.courseDBList[i]))

    # [1] Success instructor->Course
    def test_ExistCourse(self):
        self.instrObj.assignInstrCourse(self.courseList[0])
        self.assertIn(self.courseList[0].databaseReference,
                      InstructorToCourse.objects.filter(course=self.courseDBList[0], instructor=self.instrDB).course,
                      "Should have linked course and instructor together")

    # [2] Adding Course not existing in DB
    def test_NotExistCourse(self):
        temp_course = CourseObj(Course(course_id=102))  # not "101", which exists already
        with self.assertRaises(ValueError, msg="can't send in non existing course, i.e., course obj"):
            self.instrObj.assignInstrCourse(temp_course)

    # [3] Adding duplicate course: (don't know why this would happen but might as well test it :P)
    def test_duplicateCourse(self):
        self.instrObj.assignInstrCourse(self.courseList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a instructor the same course twice"):
            self.instrObj.assignInstrCourse(self.courseList[0])

    # [4] Adding Course to instructor @ max capacity
    def test_OverCap(self):
        self.instrObj.assignInstrCourse(self.courseList[0])
        self.instrObj.assignInstrCourse(self.courseList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max instructor assignments"):
            self.instrObj.assignInstrCourse(self.courseList[2])

    # [5] Trying to add a non-course
    def test_NonCourse(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(ValueError, msg="Shouldn't be allowed to assign instructor to non-course"):
                    self.instrObj.assignInstrCourse(invalid_input)


class TestInstructorGetInstrCourseAssignments(TestCase):  # Kiran
    instrDB = None
    courseDB = None
    course = None
    user = None  # for TA
    instrObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=2)  # max 2 assignment!
        self.instrObj = InstructorObj(self.instrDB)  # creating TA object using TA in database
        temp_user_for_admin = User(email_address="admin@example.com")
        temp_admin = Administrator(user=temp_user_for_admin)
        self.adminObj = AdminObj(temp_admin)

        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )
        self.course = CourseObj(self.courseDB)

    # [1] 1 assignment
    def test_1Assignment(self):
        InstructorToCourse.objects.create(course_id=self.courseDB, ta=self.instrDB)  # creating assignment?
        self.assertEquals(self.instrObj.getInstrCrseAsgmts(), 1, msg="should be 1 assigment")

    # [2] 0 assignment
    def test_0Assignment(self):
        self.assertEquals(self.instrObj.getInstrCrseAsgmts(), 0, msg="should be 0 assignments")

    # [3] 1->0 Assignment
    # using views methods: same reasoning given ^
    def test_1to0Assignment(self):
        self.instrObj.assignInstrCourse(self.course)
        self.adminObj.removeCourse(self.course)
        self.assertEquals(self.instrObj.getInstrCrseAsgmts(), 0, msg="added then removed course, should be 0")


class TestInstructorAssignInstrLec(TestCase):  # Kiran
    instrDB = None
    courseDBList = list()  # just for section
    sectionDBList = list()  # just for lec
    lecDBList = list()
    lecList = list()
    user = None  # for instructor
    instrObj = None

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TA_password',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=2)  # max 2 assignment!
        self.instrObj = InstructorObj(self.instrDB)

        for i in [1, 2, 3]:  # courses
            self.courseDBList.append(Course.objects.create(
                course_id=100 + i,
                semester='Fall 2023',
                name='Introduction to Testing',
                description='A course about writing tests in Django.',
                num_of_sections=3,
                modality='Online',
                credits=4
            ))
        for i in [1, 2, 3]:  # section
            self.sectionDBList.append(Section.objects.create(
                section_id=100 + i,
                course=self.courseDBList[i],
                location="location" + str(i),
                meeting_time="mt" + str(i)
            ))
        for i in [1, 2, 3]:  # lec
            self.lecDBList.append(Lecture.objects.create(section_id=self.sectionDBList[i]))
            self.lecList.append(self.lecDBList[i])

    # [1] Success Instructor->Lec
    def test_ExistLec(self):
        self.instrObj.assignInstrLecture(self.lecList[0])
        self.assertIn(self.instrObj.database, Lecture.objects.get(instructor=self.instrDB).instructor,
                      "Should have linked lecture and instructor together")

    # [2] Adding Lecture not existing in DB
    def test_NotExistLec(self):
        temp_lec = LectureObj(Lecture(section=self.sectionDBList[0]))  # created, not saved to db
        with self.assertRaises(ValueError, msg="can't send in non existing lecture, i.e., lecture obj"):
            self.instrObj.assignInstrLecture(temp_lec)

    # [3] Adding duplicate lecture: (don't know why this would happen but might as well test it :P)
    def test_duplicateLec(self):
        self.instrObj.assignInstrLecture(self.lecList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a instructor the same lecture twice"):
            self.instrObj.assignInstrLecture(self.lecList[0])

    # [4] Adding Instructor to lecture @ max cap
    def test_OverCap(self):
        self.instrObj.assignInstrLecture(self.lecList[0])
        self.instrObj.assignInstrLecture(self.lecList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max TA assignments"):
            self.instrObj.assignInstrLecture(self.lecList[2])

    # [5] Trying to add a non-lec
    def test_NonLec(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(TypeError, msg="Shouldn't be allowed to assign instructor to non-section"):
                    self.instrObj.assignInstrLecture(invalid_input)


class TestInstructorGetInstrLecAssignments(TestCase):  # Kiran
    instrDB = None
    lecDB = None
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
            phone_number='1234567890'
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=2)  # max 2 assignment!
        self.instrObj = InstructorObj(self.instrDB)
        temp_user_for_admin = User(email_address="admin@example.com")  # HOPEFULLY OK W/O FIELDS?
        temp_admin = Administrator(user=temp_user_for_admin)
        self.adminObj = AdminObj(temp_admin)

        # Course
        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4)
        # Section
        self.sectionDB = Section.objects.create(
            section_id=100 + 1,
            course=self.courseDB,
            location="location" + str(1),
            meeting_time="mt" + str(1))
        # Lecture
        self.lecDB = Lecture.objects.create(section_id=self.sectionDB)

    # [1] 1 lecture assignment
    def test_1Assignment(self):
        Lecture.objects.create(section_id=self.sectionDB, ta=self.instrDB)  # creating assignment?
        self.assertEquals(self.instrObj.getInstrLecAsgmts(), 1, msg="should be 1 assigment")

    # [2] 0 lab assignment
    def test_0Assignment(self):
        self.assertEquals(self.instrObj.getInstrLecAsgmts(), 0, msg="should be 0 assignments")

    # [3] 1 lab "assignment" - not in db
    def test_1AssignmentNoExistLab(self):
        temp_section = Section(section_id=102)  # not "101", which exists already HOPEFULLY OK W/O ALL FIELDS?
        temp_lec = LectureObj(Lecture(section=temp_section))

        self.instrObj.assignInstrCourse(temp_lec)
        self.assertEquals(self.instrObj.getInstrLecAsgmts(), 0, msg="shouldn't assign non-existing lecture")

    # [4] 1->0 lec Assignment
    def test_1to0Assignment(self):
        self.instrObj.assignInstrCourse(self.lecDB)
        self.adminObj.removeSection(self.lecDB)
        self.assertEquals(self.instrObj.getInstrLecAsgmts(), 0, msg="added then removed lecture, should be 0")


# don't think this is needed for our sprint 1?
class TestInstructorLecTAAssignment(TestCase):  # is this an instructor assigning a TA to a lecture?
    pass


# don't think this is needed for our sprint 1?
class TestInstructorLabTAAssignment(TestCase):  # is this an instructor assigning a TA to a lab?
    pass


class TestCourseInit(TestCase):
    pass


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
            modality='Online',
            credits=4
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

        # Attempt to add an additional instructor
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
            modality='Hybrid',
            credits=3
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
            ta=self.ta.ta_database,  # Use the underlying TA database model instance
            course=self.hold_course
        ).exists()
        self.assertTrue(ta_to_course_exists, "TA was not added to the course")

    def test_add_ta_at_max_assignments(self):
        self.ta.ta_database.max_assignments = 0  # Assume max assignments are now full
        self.ta.ta_database.save()
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

        # Attempt to add an additional TA
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
            modality='In-person',
            credits=3
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
            modality='Remote',
            credits=2
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
            modality='Mixed',
            credits=3
        )
        self.tempCourse = CourseObj(self.hold_course)
        self.new_info = {"semester": "Spring 2026", "name": "Advanced Testing Fundamentals", "description": "new",
                         "num_of_section": 3, "modality": "Online", "credits": 6}

    def test_edit_course_info(self):
        # Correct the key in new_info dictionary
        self.new_info = {"semester": "Spring 2026", "name": "Advanced Testing Fundamentals", "description": "new",
                         "num_of_sections": 3, "modality": "Online", "credits": 6}
        self.tempCourse.editCourse(self.new_info)
        self.hold_course.refresh_from_db()
        self.assertEqual(self.hold_course.semester, self.new_info["semester"], "Course semester was not updated")
        self.assertEqual(self.hold_course.name, self.new_info["name"], "Course name was not updated")
        self.assertEqual(self.hold_course.description, self.new_info["description"],
                         "Course description was not updated")
        self.assertEqual(self.hold_course.num_of_sections, self.new_info["num_of_sections"],
                         "Course section was not updated")
        self.assertEqual(self.hold_course.modality, self.new_info["modality"], "Course modality was not updated")
        self.assertEqual(self.hold_course.credits, self.new_info["credits"], "Course credits was not updated")

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
            modality='Online',
            credits=4
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
        instructor1_assignment = InstructorToCourse.objects.get(instructor=self.instructor_obj1.instr_database)
        instructor2_assignment = InstructorToCourse.objects.get(instructor=self.instructor_obj2.instr_database)

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
            modality='Remote',
            credits=3
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
            modality='Hybrid',
            credits=3
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
            modality='Remote',
            credits=2
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
        self.assertEqual(info['credits'], self.hold_course.credits, "Course credits is incorrect")


class TestSectionGetID(TestCase):  # Joe
    lab = None
    course = None

    def setUp(self):
        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        self.course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        self.lab = LabObj(tmp_section)

    def test_get_id(self):
        self.assertEquals(self.lab.getID(), 1011, "getID() did not retrieve correct section_id")

    def test_get_but_no_id(self):
        tmp_section = Section.objects.create(
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        self.lab = LabObj(tmp_section)
        self.assertIsNone(self.lab.getID(), "getID() returns an ID when none assigned")

    # Maybe test for section_id = None, but I don't think section can be made without


class TestSectionGetParentCourse(TestCase):  # Joe
    lab = None
    course = None

    # noinspection DuplicatedCode
    def setUp(self):
        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        self.course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        self.lab = LabObj(tmp_section)

    def test_get_parent_course(self):
        self.assertEquals(self.lab.getParentCourse(), self.course,
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

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

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
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
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
        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        self.lab.ta = self.ta
        self.lab.save()

        self.labObj = LabObj(self.lab)  # Form lab after adding TA manually

        self.assertEquals(
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
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmp_lab = Lab.objects.create(
            section=tmp_section,
        )

        self.lab = LabObj(tmp_lab)

    def test_add_ta(self):
        self.lab.addTA(TAObj(self.ta))
        self.assertEquals(self.ta, self.lab.getLabTAAsgmt(),
                          "addTA() does not add TA to lab")

    def test_add_ta_but_full(self):
        temp2 = User(email_address="test2@test.com", password="password2", first_name="first2", last_name="last2",
                     home_address="Your mom's house", phone_number=1234567890)

        temp_ta = TA.objects.create(user=temp2)
        self.lab.addTA(TAObj(self.ta))
        with self.assertRaises(RuntimeError, msg="Tried to add TA to full Lab"):
            self.lab.addTA(TAObj(temp_ta))


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

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

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

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        self.lecture = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta,
            instructor=tmp_instructor
        )

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

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta
        )

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        self.instructor = Instructor.objects.create(
            user=temp_user2
        )
        self.instructor.save()

        self.lecture = LectureObj(tmp_lec)

    def test_get_instructor(self):
        self.lecture.addInstr(self.instructor)
        self.assertEquals(self.instructor, self.lecture.getLecInstrAsmgt(),
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
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmp_lec = Lecture.objects.create(
            section=tmp_section
        )

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
        self.assertEquals(
            self.lecture.getLecInstrAsmgt(),
            self.instructor,
            "getLecInstrAssignment() Did not add instructor to lecture"
        )


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

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta,
            instructor=tmp_instructor
        )

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

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=self.ta,
            instructor=tmp_instructor
        )

        self.lecture = LectureObj(tmp_lec)

    def test_get_ta_assignment(self):
        self.assertEquals(
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

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        self.ta = TAObj(tmp_ta)

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=self.ta,
            instructor=tmp_instructor
        )

        self.lecture = LectureObj(tmp_lec)

    def test_add(self):
        self.lecture.addTA(self.ta)
        self.assertEquals(self.lecture.getLectureTAAsgmt(), self.ta, "addTA() did not add correct TA to lecture")

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

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta,
            instructor=tmp_instructor
        )

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
