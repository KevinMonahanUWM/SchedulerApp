from django.test import TestCase

from TAScheduler.models import User, Instructor, Course, InstructorToCourse


class SuccessfulCreation(TestCase):
    user = None
    instructor = None
    course = None
    instrToCourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="instructor@class.com", password="password", first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.instructor = Instructor.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.instrToCourse = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)

    # /home/managecourse/addinstructor
    def test_creation(self):
        temp = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)
        self.assertIsNotNone(temp, "Did not make InstructorToCourse")
        self.assertEqual(temp.instructor, self.instructor, "Instructor is not correct instructor")
        self.assertEqual(temp.course, self.course, "Course is not correct course")


class NoInstructor(TestCase):
    user = None
    instructor = None
    course = None
    instrToCourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="instructor@class.com", password="password",
                                        first_name="first", last_name="last", home_address="there",
                                        phone_number=1234567890)

        self.instructor = Instructor.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.instrToCourse = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)

    def test_no_instructor(self):
        temp = InstructorToCourse.objects.create(course=self.course)
        self.assertIsNone(temp.instructor, "No instructor has instructor")


class NoCourse(TestCase):
    user = None
    instructor = None
    course = None
    instrToCourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="instructor@class.com", password="password",
                                        first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.instructor = Instructor.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.instrToCourse = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)

    def test_no_course(self):
        temp = InstructorToCourse.objects.create(instructor=self.instructor)
        self.assertIsNone(temp.course, "No course has course")


class InstructorNoRoom(TestCase):
    user = None
    instructor = None
    course = None
    instrToCourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="instructor@class.com", password="password",
                                        first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.instructor = Instructor.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.instrToCourse = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)

    def test_instructor_no_room(self):
        tempinstructor = Instructor.objects.create(user=self.user, max_assignments=0)
        temp = InstructorToCourse.objects.create(instructor=tempinstructor, course=self.course)

        # should fail and not make I think but IDK how
        # InstructorToCourse.objects has error: Expected type 'Iterable | Container', got 'Manager' instead
        self.assertNotIn(temp, InstructorToCourse.objects, "InstructorToCourse was made when instructor at max courses")


class InstructorDeletion(TestCase):
    user = None
    instructor = None
    course = None
    instrToCourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="instructor@class.com", password="password",
                                        first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.instructor = Instructor.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.instrToCourse = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)

    def test_instructor_deletion(self):
        temp = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)
        self.instructor.delete()
        self.assertIsNone(temp, "Instructor to Course link should have deleted when instructor was deleted")


class CourseDeletion(TestCase):
    user = None
    instructor = None
    course = None
    instrToCourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="instructor@class.com", password="password",
                                        first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.instructor = Instructor.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.instrToCourse = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)

    def test_course_deletion(self):
        temp = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)
        self.course.delete()
        self.assertIsNone(temp, "Instructor to Course link should have deleted when course was deleted")
