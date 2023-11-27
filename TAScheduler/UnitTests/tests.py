import datetime

from django.test import TestCase
from TAScheduler.models import Course, User, TA, Section, Lab, Administrator, Instructor, InstructorToCourse, TAToCourse, Lecture
from TAScheduler.views_methods import UserObj, CourseObj, AdminObj, TAObj, LabObj, InstructorObj, SectionObj


# SEE METHOD DESCRIPTIONS FOR GUIDE ON HOW TO WRITE.
# Feel free to make suggestions on discord (add/remove/edit methods)!.
### Rememeber: These methods were made before any coding (I was guessing) so it's likely they should be changed.

class TestUserLogin(TestCase): # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_info = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_info)

    def test_login_valid_credentials(self):
        result = self.adminObj.login("test@example.com", "password123")
        self.assertRedirects(result, '/home/', msg="login with vaild credentials failed to redirect to home")

    def test_login_invalid_credentials(self):
        result = self.userObj.login("test@example.com", "wrongpassword")
        self.assertRedirects(result, '/', msg="incorrect password failed to redirect to login")
class TestUserGetID(TestCase): # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="adminpass",
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
class TestUserGetPassword(TestCase): # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_info = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_info)

    def test_get_password(self):
        self.assertEqual(self.adminObj.getPassword(), "password123", msg="user.getPassword failed to retrieve password")
class TestUserGetName(TestCase): # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_info = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_info)
    def test_get_name(self):
        self.assertEqual(self.adminObj.getName(), "Test User", msg="user.getName failed to retrieve name")
class TestUserGetRole(TestCase): # Alec
    def setUp(self):
        admin_user_info = User.objects.create(
            email_address="admin@example.com",
            password="adminpass",
            first_name="Admin",
            last_name="User",
            home_address="123 Admin Street",
            phone_number=1234567890
        )
        admin_info = Administrator.objects.create(user=admin_user_info)
        self.adminObj = AdminObj(admin_info)
    def test_get_role(self):
        self.assertEqual(self.adminObj.getRole(), "admin", msg="user.getRole failed to retrieve 'admin'")
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
        self.assertEqual(self.adminObj.user.email_address, "admin@example.com", msg="failed to initialize admin")
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
        self.course_info = {
            'course_id': 101,
            'semester': 'Fall 2023',
            'name': 'Intro to Testing',
            'description': 'A course about unit testing',
            'num_of_sections': 3,
            'modality': 'Online',
            'credits': 4
        }
    def test_create_course(self):
            created_course = self.adminObj.createCourse(self.course_info)
            self.assertIsNotNone(created_course)
            self.assertEqual(created_course.name, 'Intro to Testing', msg="failed to create course")
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
        user_info = User.objects.create(
            email_address='newuser@example.com',
            password= 'password123',
            first_name= 'New',
            last_name= 'User',
            home_address= '123 New Street',
            phone_number= 9876543210
        )
        created_user = self.adminObj.createUser(user_info, role='TA')
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email_address, 'newuser@example.com', msg="user not created")
class TestAdminCreateSection(TestCase):
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
        self.section_info = {
            'section_id': 201,
            'course': self.course,
            'location': 'Room 101',
            'meeting_time': datetime.datetime.now()
        }

    def test_create_section(self):
        created_section = self.adminObj.createSection(self.section_info)
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
            password='adminpassword',
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
        self.assertNotIn(self.hold_course, Course.objects, "Did not remove course from the database")

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
            password='kevpassword',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number='1234667890'
        )
        temp_ta = TA.objects.create(user=self.hold_user, grader_status=False)
        self.tempTA = TAObj(temp_ta)
        temp = User.objects.create(
            email_address='admin@example.com',
            password='adminpassword',
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
        self.assertNotIn(self.hold_user, User.objects, "Did not remove user from the database")

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
            password='adminpassword',
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
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.new_info = {"course id", 103,
                         "semester", "Spring 2024",
                         "name", "Intro to Units",
                         "description", "Unit testing at its finest",
                         "num of sections", 4,
                         "modality", "",
                         "credits", 3}

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
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.new_info = {"section id", 1012,
                         "location", "Somewhere in the universe",
                         "meeting time", datetime.datetime}

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
            password='kevpassword',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number='1234667890'
        )
        temp_ta = TA.objects.create(user=self.hold_user, grader_status=False)
        self.tempTA = TAObj(temp_ta)
        hold_user = User(
            email_address='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)
        self.new_info = {"grader status", True,
                         "max assignments", 3,
                         "first name", "Paul",
                         "last name", "Different"}

    def test_bad_course(self):
        with self.assertRaises(TypeError, msg='User that was passed is not a valid user'):
            self.admin.editUser(11, self.new_info)

    def test_bad_info(self):
        with self.assertRaises(TypeError, msg='Improper input entered for editing user'):
            self.admin.editUser(self.tempTA, 11)

    def test_success(self):
        self.admin.editUser(self.tempTA, self.new_info)
        self.assertEqual(self.new_info["first name"], Section.objects.get(section_id=1012))


class TestAdminCourseInstrAsgmt(TestCase):  # Kevin
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
            password='kevpassword',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number='1234667890'
        )
        self.hold_instr = Instructor.objects.create(user=self.hold_user)
        self.tempInstr = InstructorObj(self.hold_instr)
        hold_user = User(
            email_address='admin@example.com',
            password='adminpassword',
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
        with self.assertRaises(RuntimeError, msg="Tried to link course to non existant user"):
            self.admin.courseInstrAsmgt(self.tempInstr, self.tempCourse)

    def test_null_course(self):
        Course.delete(self.hold_course)
        with self.assertRaises(RuntimeError, msg="Tried to link user to non existant course"):
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


class TestAdminCourseTAAsgmt(TestCase):  # Kevin
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
            password='kevpassword',
            first_name='Kevin',
            last_name='User',
            home_address='123 Kevin St',
            phone_number='1234667890'
        )
        self.hold_ta = TA.objects.create(user=self.hold_user, grader_status=True)
        self.tempTA = TAObj(self.hold_ta)
        hold_user = User(
            email_address='admin@example.com',
            password='adminpassword',
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
        with self.assertRaises(RuntimeError, msg="Tried to link course to non existant user"):
            self.admin.courseTAAsmgt(self.tempTA, self.tempCourse)

    def test_null_course(self):
        Course.delete(self.hold_course)
        with self.assertRaises(RuntimeError, msg="Tried to link user to non existant course"):
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
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        self.ta_database = TA.objects.create(user=self.user, grader_status=False)

    def test_bad_input(self):
        with self.assertRaises(TypeError, msg='TA that was passed is not a valid TA'):
            ta = TAObj(11)

    def test_null_ta(self):
        User.delete(self.user)
        with self.assertRaises(TypeError, msg='TA that was passed does not exist'):
            ta = TAObj(self.ta_database)

    def test_success(self):
        ta = TAObj(self.ta_database)
        self.assertEqual(ta.ta_database, self.ta_database,
                         "TA object should be saved in the database reference")


class TestTAHasMaxAsgmts(TestCase):  # Kiran
    taDB = None
    courseDB = None
    user = None  # for TA
    taObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TApassword',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database.
        tempUserForAdmin = User(email_address='admin@example.com',
                                password='adminpassword',
                                first_name='Admin',
                                last_name='User',
                                home_address='123 Admin St',
                                phone_number='1234567890')
        tempAdmin = Administrator(user=tempUserForAdmin)
        self.adminObj = AdminObj(tempAdmin)

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
    def test_1Crse1MaxCap(self):
        TAToCourse.objects.create(ta=self.taDB, course=self.courseDB)  # assigning TA to course using db?
        self.assertEquals(self.taObj.hasMaxAsgmts(), True,
                          msg="TA has 1 max assignments & assigned 1 course: @ max cap")

    # 2] TA w/ 0 course assignment
    def test_0Crse1MaxCap(self):
        self.assertEquals(self.taObj.hasMaxAsgmts(), False,
                          msg="TA has 1 max assignments & not assigned 1 course: not @ max cap")

    # 3] TA w/ max cap -> no max assign
    # using views method: I know bad practice but this is still a good test to ensure both method's working correctly
    def test_origMaxCapToNoAsgn(self):
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
            password='TApassword',
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

    # 1] Success TA->Course
    def test_ExistCourse(self):
        self.taObj.assignTACourse(self.courseList[0])
        self.assertIn(self.courseDBList[0], TAToCourse.objects.filter(course=self.courseDBList[0], ta=self.taDB).course
                      , "Should have linked course and TA together")

    # 2] Adding Course not existing in DB
    def test_NotExistCourse(self):
        tempCourse = CourseObj(Course(course_id=104, semester='Fall 2023',
                                      name='Introduction to Testing',
                                      description='A course about writing tests in Django.',
                                      num_of_sections=3,
                                      modality='Online',
                                      credits=4))  # id =104, not 101,102,103
        with self.assertRaises(ValueError, msg="can't send in non existing course, i.e., course obj"):
            self.taObj.assignTACourse(tempCourse)

    # 3] Adding duplicate course
    def test_duplicateCourse(self):
        self.taObj.assignTACourse(self.courseList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a TA the same course twice"):
            self.taObj.assignTACourse(self.courseList[0])

    # 4] Adding Course to TA @ maxcap
    def test_OverCap(self):
        self.taObj.assignTACourse(self.courseList[0])
        self.taObj.assignTACourse(self.courseList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max TA assignments"):
            self.taObj.assignTACourse(self.courseList[2])

    # 5] Trying to add a non-course
    def test_NonCourse(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(TypeError, msg="Shouldn't be allowed to assign TA to non-course"):
                    self.taObj.assignTACourse(invalid_input)


class TestTAGetTACrseAsgmts(TestCase):  # Kiran
    taDB = None
    courseDB = None
    course = None
    user = None  # for TA
    taObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TApassword',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database.
        tempUserForAdmin = User(email_address="admin@example.com")
        tempAdmin = Administrator(user=tempUserForAdmin)
        self.adminObj = AdminObj(tempAdmin)

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

    # 1] 1 assignment
    def test_1Assignment(self):
        self.taObj.assignTACourse(self.course)
        self.assertEquals(self.taObj.getTACrseAsgmts(), 1, msg="should be 1 assigment")

    # 2] 0 assignment
    def test_0Assignment(self):
        self.assertEquals(self.taObj.getTACrseAsgmts(), 0, msg="should be 0 assigments")

    # 3] 1->0 Assignment
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
            password='TApassword',
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

    # 1] Success TA->Lab
    def test_ExistLab(self):
        self.taObj.assignTALab(self.labList[0])
        self.assertIn(self.taObj.databaseReference, Lab.objects.get(ta=self.taDB).ta
                      , "Should have linked lab and TA together")

    # 2] Adding Lab not existing in DB
    def test_NotExistLab(self):
        tempLab = LabObj(Lab(section=self.sectionDBList[0]))  # created, not saved to db
        with self.assertRaises(ValueError, msg="can't send in non existing lab, i.e., lab obj"):
            self.taObj.assignTALab(tempLab)

    # 3] Adding duplicate lab: (don't know why this would happen but might as well test it :P)
    def test_duplicateLab(self):
        self.taObj.assignTALab(self.labList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a TA the same lab twice"):
            self.taObj.assignTALab(self.labList[0])

    # 4] Adding TA to Lab @ max cap
    def test_OverCap(self):
        self.taObj.assignTALab(self.labList[0])
        self.taObj.assignTALab(self.labList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max TA assignments"):
            self.taObj.assignTALab(self.labList[2])

    # 5] Trying to add a non-lab
    def test_NonLab(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(ValueError, msg="Shouldn't be allowed to assign TA to non-course"):
                    self.taObj.assignTALab(invalid_input)

    # 6] Assigning lab TA w/ grader status
    def test_GraderStatus(self):
        tempUser = User.objects.create(email_address='grader@gmail.com', password='TApassword',
                                       first_name='TA',
                                       last_name='User',
                                       home_address='123 TA St',
                                       phone_number='1234567890')  # HOPEFULLY DON'T NEED ALL FIELDS?
        tempTa = TA.objects.create(user=tempUser, max_assignments=2, grader_status=True)  # new TA in db W/ GraderStatus
        self.taObj = TAObj(tempTa)
        with self.assertRaises(RuntimeError, msg="TA can't assign to lab when grader"):
            self.taObj.assignTALab(self.labList[0])


class TestTAGetTALabAsgmts(TestCase):  # Kiran
    taDB = None
    labDB = None
    lab = None
    user = None  # for TA
    taObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TApassword',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.taObj = TAObj(self.taDB)
        tempUserForAdmin = User(email_address="admin@example.com")  # HOPEFULLY OK W/O FIELDS?
        tempAdmin = Administrator(user=tempUserForAdmin)
        self.adminObj = AdminObj(tempAdmin)

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


    # 1] 1 lab assignment
    def test_1Assignment(self):
        Lab.objects.create(section_id=self.sectionDB, ta=self.taObj) #creating assignment?
        self.assertEquals(self.taObj.getTALabAsgmts(), 1, msg="should be 1 assigment")

    # 2] 0 lab assignment
    def test_0Assignment(self):
        self.assertEquals(self.taObj.getTALabAsgmts(), 0, msg="should be 0 assigments")

    # 3] 1 lab "assignment" - not in db
    def test_1AssignmentNoExistLab(self):
        tempSection = Section(section_id=102, course_id=self.courseDB)  # not "101", which exists already HOPEFULLY OK W/O ALL FIELDS?
        tempLab = Lab(section=tempSection, ta=self.taObj)
        self.assertEquals(self.taObj.getTALabAsgmts(), 0, msg="shouldn't assign non-existing lab")

    # 4] 1->0 lab Assignment
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
            password='TApassword',
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

    # 1] Success TA->Lec
    def test_ExistLLec(self):
        self.taObj.assignTALecture(self.lecList[0])
        self.assertIn(self.taObj.databaseReference, Lecture.objects.get(ta=self.taDB).ta
                      , "Should have linked lec and TA together")

    # 2] Adding Lec not existing in DB
    def test_NotExistLec(self):
        tempLec = LectureObj(Lecture(section=self.sectionDBList[0]))  # created, not saved to db
        with self.assertRaises(ValueError, msg="can't send in non existing lecture, i.e., lecture obj"):
            self.taObj.assignTALecture(tempLec)

    # 3] Adding duplicate lec: (don't know why this would happen but might as well test it :P)
    def test_duplicateLec(self):
        self.taObj.assignTALecture(self.lecList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a TA the same lec twice"):
            self.taObj.assignTALecture(self.lecList[0])

    # 4] Adding TA to Lab @ max cap
    def test_OverCap(self):
        self.taObj.assignTALecture(self.lecList[0])
        self.taObj.assignTALecture(self.lecList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max TA assignments"):
            self.taObj.assignTALecture(self.lecList[2])

    # 5] Trying to add a non-lec.
    def test_NonLab(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types
        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(ValueError, msg="Shouldn't be allowed to assign TA to non-course"):
                    self.taObj.assignTALecture(invalid_input)

    # 6] Assigning lec TA w/o grader status
    def test_GraderStatus(self):
        tempUser = User.objects.create(email_address='grader@gmail.com')  # HOPEFULLY DON'T NEED ALL FIELDS?
        tempTa = TA.objects.create(user=tempUser, max_assignments=2, grader_status=False)  # w/o GraderStatus
        self.taObj = TAObj(tempTa) # reassigning
        with self.assertRaises(ValueError, msg="TA can't assign to lec when grader"):
            self.taObj.assignTALecture(self.lecList[0])


class TestTAGetTALecAsgmts(TestCase):  # Kiran
    taDB = None
    lecDB = None
    user = None  # for TA
    taObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TApassword',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.taDB = TA.objects.create(user=self.user, max_assignments=1, grader_status=True)  # gs=T, max 1 assignment!
        self.taObj = TAObj(self.taDB)
        tempUserForAdmin = User(email_address="admin@example.com")  # HOPEFULLY OK W/O FIELDS?
        tempAdmin = Administrator(user=tempUserForAdmin)
        self.adminObj = AdminObj(tempAdmin)

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


    # 1] 1 lect assignment
    def test_1Assignment(self):
        Lecture.objects.create(section_id=self.sectionDB, ta=self.taDB)  # creating assignment?
        self.assertEquals(self.taObj.getTALecAsgmts(), 1, msg="should be 1 assigment")

    # 2] 0 lab assignment
    def test_0Assignment(self):
        self.assertEquals(self.taObj.getTALabAsgmts(), 0, msg="should be 0 assigments")

    # 3] 1 lab "assignment" - not in db
    def test_1AssignmentNoExistLab(self):
        tempSection = Section(section_id=102)  # not "101", which exists already HOPEFULLY OK W/O ALL FIELDS?
        tempLec = LectureObj(Lecture(section=tempSection))
        self.taObj.assignTALecture(tempLec)
        self.assertEquals(self.taObj.getTALecAsgmts(), 0, msg="shouldn't assign non-existing lecture")

    # 4] 1->0 lab Assignment
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
                password='TApassword',
                first_name='TA',
                last_name='User',
                home_address='123 TA St',
                phone_number='1234567890')
            )
        self.taDB1 = TA.objects.create(user=self.userDBList[0], max_assignments=1, grader_status=True)
        self.taDB2 = TA.objects.create(user=self.userDBList[1], max_assignments=1, grader_status=False)
        self.taObj1 = TAObj(self.taDB1)  # grader
        self.taObj2 = TAObj(self.taDB2)  # non-grader

    # 1] Getting nongrader status
    def test_nonGraderStatus(self):
        self.assertEquals(self.taObj1.getGraderStatus(), True, msg="grader status ta should have true GS field")

    # 2] Getting grader status
    def test_graderStatus(self):
        self.assertEquals(self.taObj2.getGraderStatus(), False, msg="non grader status ta should have false GS field")


class TestInstructorInit(TestCase):
    instructorDB = None
    user = None
    instrObj = None

    def setUp(self):
        self.user = User.objects.create(
            email_address='admin@example.com',
            password='adminpassword',
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
        User.objects.get(email_address = 'admin@example.com').delete()
        with self.assertRaises(TypeError, msg='instructor that was passed does not exist'):
            self.instrObj = InstructorObj(self.instructorDB)

    def test_success(self):
        self.instrObj = InstructorObj(self.instructorDB)
        self.assertEqual(self.instrObj.databaseReference, self.instructorDB,
                         msg="insrtuctor object should be saved in the database reference")


class TestInstructorHasMaxAsgmts(TestCase):  # Kiran
    instrDB = None
    courseDB = None
    user = None  # for instructor
    instrObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TApassword',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.instrObj = InstructorObj(self.instrDB)
        tempUserForAdmin = User(email_address="admin@example.com")
        tempAdmin = Administrator(user=tempUserForAdmin)
        self.adminObj = AdminObj(tempAdmin)

        self.courseDB = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )

    # 1] Instr w/ 1 course assignment
    def test_1Crse1MaxCap(self):
        InstructorToCourse.objects.create(instructor=self.instrDB, course=self.courseDB)
        self.assertEquals(self.instrObj.hasMaxAsgmts(), True,
                          msg="instructor has 1 max assignments & assigned 1 course: @ max cap")

    # 2] Instr w/ 0 course assignment
    def test_0Crse1MaxCap(self):
        self.assertEquals(self.instrObj.hasMaxAsgmts(), False,
                          msg="instructor has 1 max assignments & not assigned 1 course: not @ max cap")

    # 3] Instr w/ max cap -> no max assign
    # using views method
    def test_origMaxCapToNoAsgn(self):
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
            password='TApassword',
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

    # 1] Success instructore->Course
    def test_ExistCourse(self):
        self.instrObj.assignInstrCourse(self.courseList[0])
        self.assertIn(self.courseList[0].databaseReference,
                      InstructorToCourse.objects.filter(course=self.courseDBList[0], instructor=self.instrDB).course
                      , "Should have linked course and instructor together")

    # 2] Adding Course not existing in DB
    def test_NotExistCourse(self):
        tempCourse = CourseObj(Course(course_id=102))  # not "101", which exists already
        with self.assertRaises(ValueError, msg="can't send in non existing course, i.e., course obj"):
            self.instrObj.assignInstrCourse(tempCourse)

    # 3] Adding duplicate course: (don't know why this would happen but might as well test it :P)
    def test_duplicateCourse(self):
        self.instrObj.assignInstrCourse(self.courseList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a instructor the same course twice"):
            self.instrObj.assignInstrCourse(self.courseList[0])

    # 4] Adding Course to instructor @ maxcap
    def test_OverCap(self):
        self.instrObj.assignInstrCourse(self.courseList[0])
        self.instrObj.assignInstrCourse(self.courseList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max instructor assignments"):
            self.instrObj.assignInstrCourse(self.courseList[2])

    # 5] Trying to add a non-course
    def test_NonCourse(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(ValueError, msg="Shouldn't be allowed to assign instructor to non-course"):
                    self.instrObj.assignInstrCourse(invalid_input)


class TestInstructorGetInstrCrseAsgmts(TestCase):  # Kiran
    instrDB = None
    courseDB = None
    course = None
    user = None  # for TA
    instrObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TApassword',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=2)  # max 2 assignment!
        self.instrObj = InstructorObj(self.instrDB)  # creating TA object using TA in database
        tempUserForAdmin = User(email_address="admin@example.com")
        tempAdmin = Administrator(user=tempUserForAdmin)
        self.adminObj = AdminObj(tempAdmin)

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

    # 1] 1 assignment
    def test_1Assignment(self):
        InstructorToCourse.objects.create(course_id=self.courseDB, ta=self.instrDB)  # creating assignment?
        self.assertEquals(self.instrObj.getInstrCrseAsgmts(), 1, msg="should be 1 assigment")

    # 2] 0 assignment
    def test_0Assignment(self):
        self.assertEquals(self.instrObj.getInstrCrseAsgmts(), 0, msg="should be 0 assigments")

    # 3] 1->0 Assignment
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
            password='TApassword',
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

    # 1] Success Instructor->Lec
    def test_ExistLec(self):
        self.instrObj.assignInstrLecture(self.lecList[0])
        self.assertIn(self.instrObj.databaseReference, Lecture.objects.get(instructor=self.instrDB).instructor
                      , "Should have linked lecture and instructor together")

    # 2] Adding Lecture not existing in DB
    def test_NotExistLec(self):
        tempLec = LectureObj(Lecture(section=self.sectionDBList[0]))  # created, not saved to db
        with self.assertRaises(ValueError, msg="can't send in non existing lecture, i.e., lecture obj"):
            self.instrObj.assignInstrLecture(tempLec)

    # 3] Adding duplicate lecture: (don't know why this would happen but might as well test it :P)
    def test_duplicateLec(self):
        self.instrObj.assignInstrLecture(self.lecList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a instructor the same lecture twice"):
            self.instrObj.assignInstrLecture(self.lecList[0])

    # 4] Adding Instructor to lecture @ max cap
    def test_OverCap(self):
        self.instrObj.assignInstrLecture(self.lecList[0])
        self.instrObj.assignInstrLecture(self.lecList[1])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max TA assignments"):
            self.instrObj.assignInstrLecture(self.lecList[2])

    # 5] Trying to add a non-lec
    def test_NonLec(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(TypeError, msg="Shouldn't be allowed to assign instructor to non-section"):
                    self.instrObj.assignInstrLecture(invalid_input)


class TestInstructorGetInstrLecAsgmts(TestCase):  # Kiran
    instrDB = None
    lecDB = None
    user = None  # for instructor
    instrObj = None
    adminObj = None  # for deleting course

    def setUp(self):
        self.user = User.objects.create(
            email_address='TA@example.com',
            password='TApassword',
            first_name='TA',
            last_name='User',
            home_address='123 TA St',
            phone_number='1234567890'
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=2)  # max 2 assignment!
        self.instrObj = InstructorObj(self.instrDB)
        tempUserForAdmin = User(email_address="admin@example.com")  # HOPEFULLY OK W/O FIELDS?
        tempAdmin = Administrator(user=tempUserForAdmin)
        self.adminObj = AdminObj(tempAdmin)

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

    # 1] 1 lecture assignment
    def test_1Assignment(self):
        Lecture.objects.create(section_id=self.sectionDB, ta=self.instrDB)  # creating assignment?
        self.assertEquals(self.instrObj.getInstrLecAsgmts(), 1, msg="should be 1 assigment")

    # 2] 0 lab assignment
    def test_0Assignment(self):
        self.assertEquals(self.instrObj.getInstrLecAsgmts(), 0, msg="should be 0 assigments")

    # 3] 1 lab "assignment" - not in db
    def test_1AssignmentNoExistLab(self):
        tempSection = Section(section_id=102)  # not "101", which exists already HOPEFULLY OK W/O ALL FIELDS?
        tempLec = LectureObj(Lecture(section=tempSection))

        self.instrObj.assignInstrCourse(tempLec)
        self.assertEquals(self.instrObj.getInstrLecAsgmts(), 0, msg="shouldn't assign non-existing lecture")

    # 4] 1->0 lec Assignment
    def test_1to0Assignment(self):
        self.instrObj.assignInstrCourse(self.lecDB)
        self.adminObj.removeSection(self.lecDB)
        self.assertEquals(self.instrObj.getInstrLecAsgmts(), 0, msg="added then removed lecture, should be 0")


# don't think this is needed for our sprint 1?
class TestInstructorLecTAAsmgt(TestCase):  # is this an instructor assigning a TA to a lecture?
    pass


# don't think this is needed for our sprint 1?
class TestInstructorLabTAAsmgt(TestCase):  # is this an instructor assigning a TA to a lab?
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
