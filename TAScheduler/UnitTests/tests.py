import datetime

from django.test import TestCase

from TAScheduler.models import Course, User, TA, Section, Lab, Administrator, InstructorToCourse, TAToCourse, Instructor
from TAScheduler.views_methods import CourseObj, AdminObj, TAObj, LabObj, InstructorObj


# PBI Assignments ...
# Alec = #1,#2 (Total = 6)
# Kevin = #3,#4,#5 (Total = 4)
# Randall = #6,#7,#8 (Total = 12)
# Kiran = #9,#10,#11 (Total = 15)
# Joe = #12,#13 (Total = 8)
# SEE METHOD DESCRIPTIONS FOR GUIDE ON HOW TO WRITE.
# Feel free to make suggestions on discord (add/remove/edit methods)!.
### Rememeber: These methods were made before any coding (I was guessing) so it's likely they should be changed.
class TestUserLogin(TestCase):  # Alec
    pass


class TestUserGetID(TestCase):  # Alec
    pass


class TestUserGetPassword(TestCase):  # Alec
    pass


class TestUserGetName(TestCase):  # Alec
    pass


class TestUserGetRole(TestCase):  # Alec
    pass


class TestAdminInit(TestCase):
    pass


class TestAdminCreateCourse(TestCase):  # Alec
    pass


class TestAdminCreateUser(TestCase):  # Alec
    pass


class TestAdminCreateSection(TestCase):  # Alec
    pass


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
            user=self.instructor_user)  # Create an Instructor model instance
        self.instructor = InstructorObj(self.instructor_model)  # Wrap it with InstructorObj

    def test_add_instructor(self):
        self.tempCourse.addInstructor(self.instructor)
        # Check if the instructor was added to the course

        instructor_to_course_exists = InstructorToCourse.objects.filter(
            instructor=self.instructor_model,  # Use the Instructor model instance
            course=self.hold_course
        ).exists()
        self.assertTrue(instructor_to_course_exists, "Instructor was not added to the course")

    def test_add_instructor_max_assignments(self):
        self.instructor.setMaxAssignments(0)  # Assuming max assignments are now full
        with self.assertRaises():
            self.tempCourse.addInstructor(self.instructor)

    def test_add_incorrect_object_as_instructor(self):
        fake_object = TAObj()
        with self.assertRaises(TypeError):
            self.tempCourse.addInstructor(fake_object)


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
        self.ta = TA.objects.create(user=self.ta_user, grader_status=False)

    def test_add_ta(self):
        self.tempCourse.addTa(self.ta)
        # Check if the TA was added to the course

        ta_to_course_exists = TAToCourse.objects.filter(
            ta=self.ta, course=self.hold_course
        ).exists()
        self.assertTrue(ta_to_course_exists, "TA was not added to the course")

    def test_add_instructor_max_assignments(self):
        # Set max assignments for the instructor to 0
        self.TA.setMaxAssignments(0)  # Implement this method in InstructorObj
        with self.assertRaises():
            self.tempCourse.addTa(self.TA)

    def test_add_incorrect_object_as_TA(self):
        fake_object = InstructorObj()
        with self.assertRaises(TypeError):
            self.tempCourse.addTA(fake_object)


class TestCourseRemoveAssignment(TestCase):  # Randall
    hold_course = None
    tempCourse = None
    ta_user = None
    ta_obj = None
    TAObj = None

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
        self.ta_user = User.objects.create(
            email_address='user@example.com',
            password='password',
            first_name='Regular',
            last_name='User',
            home_address='123 User St',
            phone_number='1234567893'
        )

        self.ta = TA.objects.create(user=self.ta_user, grader_status=False)
        self.ta_obj = TAObj(self.ta)

    def test_remove_assignment(self):
        self.tempCourse.removeAssignment(self.ta_obj)
        # Check if the assignment (user) was removed from the course
        assignments = self.tempCourse.getAsgmtsForCrse()
        self.assertNotIn(self.ta_obj, assignments, "User was not removed from the course assignments")
        self.assertTrue(self._obj not in assignments or assignments is None, "Tried to remove TA with no assignments")


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
        incorrect_info = {"semester": 2026, "name": 123, "description": True}
        with self.assertRaises(ValueError):
            self.tempCourse.editCourse(incorrect_info)


class TestCourseGetAsgmtsForCrse(TestCase):  # Randall
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

    def test_get_assignments_for_course(self):
        assignments = self.tempCourse.getAsgmtsForCrse()
        # Assertions to verify the correct assignments are returned
        self.assertIn(self.user1, assignments, "User1 is not in the course assignments")
        self.assertIn(self.user2, assignments, "User2 is not in the course assignments")


class TestCourseGetSectionsForCrse(TestCase):  # Randall
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
        # Add some sections to the course
        self.section1 = Section.objects.create(section_id=201, course=self.hold_course)
        self.section2 = Section.objects.create(section_id=202, course=self.hold_course)

    def test_get_sections_for_course(self):
        sections = self.tempCourse.getSectionsCrse()
        self.assertIn(self.section1, sections, "Section1 is not in the course sections")
        self.assertIn(self.section2, sections, "Section2 is not in the course sections")


class TestCourseGetCrseInfo(TestCase):  # Randall
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
        self.assertEqual(info['num_of_section'], self.hold_course.num_of_sections, "Course section is incorrect")
        self.assertEqual(info['modality'], self.hold_course.modality, "Course modality is incorrect")
        self.assertEqual(info['credits'], self.hold_course.credits, "Course credits is incorrect")


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
