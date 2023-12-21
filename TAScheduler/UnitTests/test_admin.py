from django.test import TestCase

from TAScheduler.models import TAToCourse, InstructorToCourse, Administrator, User, Instructor, Course, TA, Section, \
    Lab, Lecture
from TAScheduler.view_methods.admin_methods import AdminObj
from TAScheduler.view_methods.course_methods import CourseObj
from TAScheduler.view_methods.instructor_methods import InstructorObj
from TAScheduler.view_methods.lab_methods import LabObj
from TAScheduler.view_methods.ta_methods import TAObj


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
            'course_id': course.course_id,
            'location': 'Room 101',
            'meeting_time': "2000-1-1 12:00:00",
            "section_type": "Lab"
        }
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
                "meeting_time": 0}
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

class TestAdminGetAllCrseAsgmts(TestCase):
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
        self.assertEqual(self.admin.getAllCrseAsgmts().get(104), ('instr1@example.com', 'ta1@example.com'), "Course 104 does not do")
        self.assertEqual(self.admin.getAllCrseAsgmts().get(102), ('instr2@example.com', 'ta2@example.com'), "Course 102 does not do")
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
                                             meeting_time="Meeting loc")
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