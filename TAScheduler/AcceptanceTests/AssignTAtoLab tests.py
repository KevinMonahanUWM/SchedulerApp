import datetime

from django.test import TestCase

from TAScheduler.models import User, TA, Course, Section, TAToSection


class InstructorToCourseTests(TestCase):
    user = None
    ta = None
    course = None
    section = None
    tatosection = None

    def setUp(self):
        self.user = User.objects.create(email_address="ta@class.com", password="password", first_name="first",
                                        last_name="last", home_address="there", phone_number=1234567890)

        self.ta = TA.objects.create(user=self.user)

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="test",
                                            description="test", num_of_sections=2, modality="online", credits=1)

        self.section = Section.objects.create(section_id=101, course=self.course, location="your mom's house",
                                              meeting_time=datetime.time)

        self.tatosection = TAToSection.objects.create(ta=self.ta, section=self.section)

    def test_creation(self):
        temp = TAToSection.objects.create(ta=self.ta, section=self.section)
        self.assertIsNotNone(temp, "TAToSection does not make anything")
        self.assertEqual(temp.section, self.section, "TAToSection does not make correct section")
        self.assertEqual(temp.ta, self.ta, "TAToSection does not make correct TA")

    def test_no_ta(self):
        temp = TAToSection.objects.create(ta=self.ta)
        self.assertIsNone(temp.ta, "TAToSection makes TA with no input")

    def test_no_section(self):
        temp = TAToSection.objects.create(section=self.section)
        self.assertIsNone(temp.section, "TAToSection makes section with no input")

    def test_ta_deletion(self):
        temp = TAToSection.objects.create(ta=self.ta, section=self.section)
        self.ta.delete()
        self.assertIsNone(temp, "TAToSection link should have deleted when TA was deleted")

    def test_section_deletion(self):
        temp = TAToSection.objects.create(ta=self.ta, section=self.section)
        self.section.delete()
        self.assertIsNone(temp, "TAToSection link should have deleted when section was deleted")
