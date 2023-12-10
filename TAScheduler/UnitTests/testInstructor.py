from datetime import datetime

from django.test import TestCase
from TAScheduler.models import Course, User, Section, Administrator, InstructorToCourse, Instructor, Lecture
from TAScheduler.views_methods import CourseObj, AdminObj, InstructorObj, LectureObj


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
            phone_number=1234567890
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.instrObj = InstructorObj(self.instrDB)
        for i in [1, 2, 3]:
            self.courseDBList.append(Course.objects.create(
                course_id=100 + i,
                semester='Fall 2023',
                name='Introduction to Testing',
                description='A course about writing tests in Django.',
                num_of_sections=3,
                modality='Online'
            ))
            self.courseList.append(CourseObj(self.courseDBList[i - 1]))

    # [1] Success instructor->Course
    def test_ExistCourse(self):
        self.instrObj.assignInstrCourse(self.courseList[0])
        self.assertEqual(self.courseDBList[0],
                         InstructorToCourse.objects.filter(course=self.courseDBList[0],
                                                           instructor=self.instrDB)[0].course,
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
        with self.assertRaises(ValueError,
                               msg="can't assign courses when already reaches the max instructor assignments"):
            self.instrObj.assignInstrCourse(self.courseList[1])

    # [5] Trying to add a non-course
    def test_NonCourse(self):
        invalid_inputs = [123, 3.14, True, [1, 2, 3], {'key': 'value'}]  # testing a bunch of different obj types

        for invalid_input in invalid_inputs:
            with self.subTest(
                    invalid_input=invalid_input):  # if 1 subtest test runs, it will continue running through loop
                with self.assertRaises(TypeError, msg="Shouldn't be allowed to assign instructor to non-course"):
                    self.instrObj.assignInstrCourse(invalid_input)

    # [2] 0 assignment
    def test_0Assignment(self):
        self.assertEquals(self.instrObj.getInstrCrseAsgmts().count(), 0, msg="should be 0 assignments")


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

    # [3] 1->0 Assignment
    # using views methods: same reasoning given ^
    def test_1to0Assignment(self):
        self.instrObj.assignInstrCourse(self.course)
        self.adminObj.removeCourse(self.course)
        self.assertQuerysetEqual(InstructorToCourse.objects.filter(instructor=self.instrDB),
                                 self.instrObj.getInstrCrseAsgmts(), msg="added then removed course, should be 0")


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
            phone_number=1234567890
        )
        self.instrDB = Instructor.objects.create(user=self.user, max_assignments=1)  # max 1 assignment!
        self.instrObj = InstructorObj(self.instrDB)
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
        for i in [1, 2]:  # lec
            self.lecDBList.append(
                Lecture.objects.create(section=self.sectionDBList[i - 1]))  # HOPEFULLY FINE W/O FIELDS?
            self.lecList.append(LectureObj(self.lecDBList[i - 1]))

    # [1] Success Instructor->Lec
    def test_ExistLec(self):
        self.instrObj.assignInstrLecture(self.lecList[0])
        self.assertEqual(self.lecDBList[0].instructor, self.instrDB, "Should have linked lec and instructor together")

    # [2] Adding duplicate lecture: (don't know why this would happen but might as well test it :P)
    def test_duplicateLec(self):
        self.instrObj.assignInstrLecture(self.lecList[1])
        with self.assertRaises(ValueError,
                               msg="violated integrity of database, can't assign a instructor the same lecture twice"):
            self.instrObj.assignInstrLecture(self.lecList[1])

    # [3] Adding Instructor to lecture @ max cap
    def test_OverCap(self):
        temp_userDB = User.objects.create(
            email_address='Instr2@example.com',  # different from "Instr@example.com"
            password='Instr_password',
            first_name='Instr',
            last_name='User',
            home_address='123 Instr St',
            phone_number=1234567890
        )
        tempInstrDB = Instructor.objects.create(user=temp_userDB, max_assignments=1)
        tempLecDB = Lecture.objects.create(
            section=self.sectionDBList[2],
            instructor=tempInstrDB)
        lec3 = LectureObj(tempLecDB)  # Lec3 = New Lec w/ New Ta assignment
        with self.assertRaises(ValueError,
                               msg="can't assign lecture when the lecture already has assignment"):
            self.instrObj.assignInstrLecture(lec3)

    # [4] Trying to add a non-lec
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
