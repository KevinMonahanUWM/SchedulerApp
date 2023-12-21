from django.test import TestCase
from TAScheduler.models import TAToCourse, Administrator, Course, User, TA, Lecture, Section, Lab
from TAScheduler.view_methods.admin_methods import AdminObj
from TAScheduler.view_methods.course_methods import CourseObj
from TAScheduler.view_methods.lab_methods import LabObj
from TAScheduler.view_methods.lecture_methods import LectureObj
from TAScheduler.view_methods.ta_methods import TAObj


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
        self.course = CourseObj(self.courseDB)

    # [1] 1 assignment
    def test_1Assignment(self):
        TAToCourse.objects.create(course=self.courseDB, ta=self.taDB)
        self.assertQuerysetEqual(TAToCourse.objects.filter(ta=self.taDB),
                                 self.taObj.getTACrseAsgmts(), msg="should be 1 assigment")

    # [2] 0 assignment
    def test_0Assignment(self):
        self.assertQuerysetEqual(TAToCourse.objects.filter(ta=self.taDB),
                                 self.taObj.getTACrseAsgmts(), msg="should be 0 assignments")


class TestTAGetTALabAssignments(TestCase):  # Kiran
    taDB = None
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
            meeting_time="Random loc"
        )
        # Lab - create assignments in the test.

    # [1] 1 lab assignment
    def test_1Assignment(self):
        Lab.objects.create(section=self.sectionDB, ta=self.taDB)
        self.assertQuerysetEqual(Lab.objects.filter(ta=self.taDB), self.taObj.getTALabAsgmts(),
                                 msg="should be 1 assigment")

    # [2] 0 lab assignment
    def test_0Assignment(self):
        qs = Lab.objects.filter(ta=self.taDB)
        self.assertQuerysetEqual(qs, self.taObj.getTALabAsgmts(),
                                 msg="should be 0 assignments")


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
            meeting_time="Rand loc"
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
        self.assertEqual(self.taObj2.getGraderStatus(), False,
                         msg="non grader status ta should have false GS field")


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
