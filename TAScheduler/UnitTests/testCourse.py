from django.test import TestCase
from TAScheduler.models import Course, User, TA, Section, InstructorToCourse, TAToCourse, Instructor
from TAScheduler.views_methods import CourseObj, TAObj,  InstructorObj
from django.core.exceptions import ValidationError


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
