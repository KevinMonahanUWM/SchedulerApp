from datetime import datetime
from django.test import TestCase
from TAScheduler.models import TAToCourse, Administrator, Course, User, TA, Lecture, Section, Lab
from TAScheduler.views_methods import CourseObj, AdminObj, TAObj, LectureObj, LabObj


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
            phone_number=1234567890
        )
        self.taDB = TA.objects.create(user=self.user, grader_status=False, max_assignments=1)  # max 1 assignment!
        self.taObj = TAObj(self.taDB)  # creating TA object using TA in database.
        for i in [1, 2, 3]:
            self.courseDBList.append(Course.objects.create(
                course_id=100 + i,
                semester='Fall 2023',
                name='Introduction to Testing',
                description='A course about writing tests in Django.',
                num_of_sections=3,
                modality='Online'
            ))
            self.courseList.append(CourseObj(self.courseDBList[i - 1]))  # NEEDED I-1

    # [1] Success TA->Course
    def test_ExistCourse(self):
        self.taObj.assignTACourse(self.courseList[0])
        self.assertEqual(self.courseDBList[0],
                         TAToCourse.objects.filter(course=self.courseDBList[0], ta=self.taDB)[0].course,
                         "Should have linked course and TA together")  # NEEDED [0]

    # [2] Adding Course not existing in DB TESTING WHY THIS IS WORKING
    def test_NotExistCourse(self):
        tempCourse = CourseObj(Course(course_id=102))  # not "101", which exists already
        with self.assertRaises(ValueError, msg="can't send in non existing course, i.e., course obj"):
            self.taObj.assignTACourse(tempCourse)

    # [3] Adding duplicate course
    def test_duplicateCourse(self):
        self.taObj.assignTACourse(self.courseList[0])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a TA the same course twice"):
            self.taObj.assignTACourse(self.courseList[0])

    # [4] Adding Course to TA @ max capacity
    def test_OverCap(self):
        self.taObj.assignTACourse(self.courseList[0])
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max TA assignments"):
            self.taObj.assignTACourse(self.courseList[1])

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

    # [3] 1->0 Assignment
    # using views method: same reasons above^
    def test_1to0Assignment(self):
        self.taObj.assignTACourse(self.course)
        self.adminObj.removeCourse(self.course)
        self.assertQuerysetEqual(TAToCourse.objects.filter(ta=self.taDB),
                                 self.taObj.getTACrseAsgmts(), msg="added then removed course, should be 0")

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
                phone_number=1234567890
            )
            self.taDB = TA.objects.create(user=self.user, grader_status=False, max_assignments=1)  # max 1 assignment!
            self.taObj = TAObj(self.taDB)  # creating TA object using TA in database.
            for i in [1, 2, 3]:
                self.courseDBList.append(Course.objects.create(
                    course_id=100 + i,
                    semester='Fall 2023',
                    name='Introduction to Testing',
                    description='A course about writing tests in Django.',
                    num_of_sections=3,
                    modality='Online'
                ))
            for i in [1, 2, 3]:  # section
                self.sectionDBList.append(Section.objects.create(
                    section_id=100 + i,
                    course=self.courseDBList[i - 1],
                    location="location" + str(i),
                    meeting_time=datetime(2023, 1, 1 + i, 12, 0, 0)
                ))
            for i in [1, 2]:  # lab
                self.labDBList.append(Lab.objects.create(
                    section=self.sectionDBList[i - 1],
                    ta=None
                ))
                self.labList.append(LabObj(self.labDBList[i - 1]))

        # [1] Success TA->Lab
        def test_ExistLab(self):
            self.taObj.assignTALab(self.labList[0])
            lab_query = Lab.objects.filter(section=self.labDBList[0].section, ta=self.taDB)
            self.assertEqual(self.labDBList[0].ta, lab_query[0].ta, "Should have linked lab and TA together")

        # [2] Adding duplicate lab: (don't know why this would happen but might as well test it :P)
        def test_duplicateLab(self):
            self.taObj.assignTALab(self.labList[1])
            with self.assertRaises(ValueError,
                                   msg="violated integrity of database, can't assign a TA the same lab twice"):
                self.taObj.assignTALab(self.labList[1])

        # [3] Adding TA to Lab @ max cap
        def test_OverCap(self):
            temp_userDB = User.objects.create(
                email_address='TA2@example.com',  # different from "TA@example.com"
                password='TA_password',
                first_name='TA',
                last_name='User',
                home_address='123 TA St',
                phone_number=1234567890
            )
            tempTADB = TA.objects.create(user=temp_userDB, grader_status=False, max_assignments=1)
            tempLabDB = Lab.objects.create(
                section=self.sectionDBList[2],
                ta=tempTADB)
            lab3 = LabObj(tempLabDB)  # Lab3 = New Lab w/ New Ta assignment
            with self.assertRaises(ValueError,
                                   msg="can't assign lab when the lab already has assignment"):
                self.taObj.assignTALab(lab3)

        # [4] Trying to add a non-lab
        def test_NonLab(self):
            invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

            for invalid_input in invalid_inputs:
                with self.subTest(
                        invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                    with self.assertRaises(TypeError, msg="Shouldn't be allowed to assign TA to non-course"):
                        self.taObj.assignTALab(invalid_input)

        # [5] Assigning lab TA w/ grader status
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
                meeting_time=datetime(2023, 1, 1, 12, 0, 0)
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

        # [3] 1->0 lab Assignment
        # Using views method: I know not good practice but this is still a good check for both of the assign/remove methods.
        def test_1to0Assignment(self):
            labDB = Lab.objects.create(section=self.sectionDB, ta=None)
            self.taObj.assignTALab(LabObj(labDB))
            self.adminObj.removeSection(LabObj(labDB))
            self.assertQuerysetEqual(Lab.objects.filter(ta=self.taDB), self.taObj.getTALabAsgmts(),
                                     msg="added then removed lab, should be 0")

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
                phone_number=1234567890
            )
            self.taDB = TA.objects.create(user=self.user, grader_status=True, max_assignments=1)  # max 1 assignment!
            self.taObj = TAObj(self.taDB)  # creating TA object using TA in database.
            for i in [1, 2, 3]:
                tmp = Course.objects.create(
                    course_id=100 + i,
                    semester='Fall 2023',
                    name='Introduction to Testing',
                    description='A course about writing tests in Django.',
                    num_of_sections=3,
                    modality='Online'
                )
                self.courseDBList.append(tmp)
                TAToCourse.objects.create(ta=self.taDB, course=tmp)
            for i in [1, 2, 3]:  # section
                self.sectionDBList.append(Section.objects.create(
                    section_id=100 + i,
                    course=self.courseDBList[i - 1],
                    location="location" + str(i),
                    meeting_time=datetime(2023, 1, 1 + i, 12, 0, 0)
                ))
            for i in [1, 2]:  # lec
                self.lecDBList.append(
                    Lecture.objects.create(section=self.sectionDBList[i - 1]))  # HOPEFULLY FINE W/O FIELDS?
                self.lecList.append(LectureObj(self.lecDBList[i - 1]))

        # [1] Success TA->Lec
        def test_ExistLLec(self):
            self.taObj.assignTALecture(self.lecList[0])
            self.assertEqual(self.lecDBList[0].ta, self.taDB, "Should have linked lec and TA together")

        # [2] Adding duplicate lec: (don't know why this would happen but might as well test it :P)
        def test_duplicateLec(self):
            self.taObj.assignTALecture(self.lecList[1])
            with self.assertRaises(ValueError,
                                   msg="violated integrity of database, can't assign a TA the same lec twice"):
                self.taObj.assignTALecture(self.lecList[1])

        # [3] Adding TA to Lecture @ max cap
        def test_OverCap(self):
            temp_userDB = User.objects.create(
                email_address='TA2@example.com',  # different from "TA@example.com"
                password='TA_password',
                first_name='TA',
                last_name='User',
                home_address='123 TA St',
                phone_number=1234567890
            )
            tempTADB = TA.objects.create(user=temp_userDB, grader_status=False, max_assignments=1)
            tempLecDB = Lecture.objects.create(
                section=self.sectionDBList[2],
                ta=tempTADB)
            lec3 = LectureObj(tempLecDB)  # Lec3 = New Lec w/ New Ta assignment
            with self.assertRaises(ValueError,
                                   msg="can't assign lecture when the lecture already has assignment"):
                self.taObj.assignTALecture(lec3)

        # [4] Trying to add a non-lec.
        def test_NonLec(self):
            invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types
            for invalid_input in invalid_inputs:
                with self.subTest(
                        invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                    with self.assertRaises(TypeError, msg="Shouldn't be allowed to assign TA to non-course"):
                        self.taObj.assignTALecture(invalid_input)

        # [5] Assigning lec TA w/o grader status
        def test_GraderStatus(self):
            temp_user = User.objects.create(email_address='NOgrader@gmail.com', password='TA_password',
                                            first_name='TA',
                                            last_name='User',
                                            home_address='123 TA St',
                                            phone_number='1234567890')  # HOPEFULLY DON'T NEED ALL FIELDS?
            tempTa = TA.objects.create(user=temp_user, max_assignments=2, grader_status=False)  # w/o GraderStatus
            tempTAObj = TAObj(tempTa)  # reassigning instance variable
            TAToCourse.objects.create(ta=tempTa, course=self.lecList[0].getParentCourse())
            with self.assertRaises(RuntimeError, msg="TA can't assign to lec when grader"):
                tempTAObj.assignTALecture(self.lecList[0])

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

        # [3] 1->0 lab Assignment
        # Using views method: I know not good practice but this is still a good check for both of the assign/remove methods.
        def test_1to0Assignment(self):
            lecDB = Lecture.objects.create(section=self.sectionDB, ta=None)
            self.taObj.assignTALecture(LectureObj(lecDB))
            self.adminObj.removeSection(LectureObj(lecDB))
            self.assertQuerysetEqual(Lecture.objects.filter(ta=self.taDB), self.taObj.getTALecAsgmts(),
                                     msg="added then removed lecture, should be 0")

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