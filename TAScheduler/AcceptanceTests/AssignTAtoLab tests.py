import datetime

from django.test import TestCase

from TAScheduler.models import User, TA, Course, TAToCourse


#
class SuccessfulAssignment(TestCase):
    user = None
    ta = None
    course = None
    tatocourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="ta@class.com", password="password", first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.ta = TA.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.tatocourse = TAToCourse.objects.create(ta=self.ta, course=self.course)

    def test_creation(self):
        temp = TAToCourse.objects.create(ta=self.ta, course=self.course)
        self.assertIsNotNone(temp, "TAToCourse does not make anything")
        self.assertEqual(temp.course, self.course, "TAToCourse does not make correct course")
        self.assertEqual(temp.ta, self.ta, "TAToCourse does not make correct TA")


class NoTA(TestCase):
    user = None
    ta = None
    course = None
    tatocourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="ta@class.com", password="password", first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.ta = TA.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.tatocourse = TAToCourse.objects.create(ta=self.ta, course=self.course)

    def test_no_ta(self):
        temp = TAToCourse.objects.create(ta=self.ta)
        self.assertIsNone(temp.ta, "TAToCourse makes TA with no input")


class NoCourse(TestCase):
    user = None
    ta = None
    course = None
    tatocourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="ta@class.com", password="password", first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.ta = TA.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.tatocourse = TAToCourse.objects.create(ta=self.ta, course=self.course)

    def test_no_course(self):
        temp = TAToCourse.objects.create(course=self.course)
        self.assertIsNone(temp.course, "TAToCourse makes course with no input")


class TaDelete(TestCase):
    user = None
    ta = None
    course = None
    tatocourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="ta@class.com", password="password", first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.ta = TA.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.tatocourse = TAToCourse.objects.create(ta=self.ta, course=self.course)

    def test_ta_deletion(self):
        temp = TAToCourse.objects.create(ta=self.ta, course=self.course)
        self.ta.delete()
        self.assertIsNone(temp, "TAToCourse link should have deleted when TA was deleted")


class CourseDelete(TestCase):
    user = None
    ta = None
    course = None
    tatocourse = None

    def setUp(self):
        self.user = User.objects.create(email_address="ta@class.com", password="password", first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.ta = TA.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.tatocourse = TAToCourse.objects.create(ta=self.ta, course=self.course)

    def test_course_deletion(self):
        temp = TAToCourse.objects.create(ta=self.ta, course=self.course)
        self.course.delete()
        self.assertIsNone(temp, "TAToCourse link should have deleted when course was deleted")
