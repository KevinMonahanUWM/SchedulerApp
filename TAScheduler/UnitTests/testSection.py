from django.test import TestCase
from TAScheduler.models import Course, User, TA, Section, Lab
from TAScheduler.views_methods import LabObj


class TestSectionGetID(TestCase):  # Joe
    lab = None
    course = None

    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        self.course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        self.lab = LabObj(Lab(section=tmp_section))

    def test_get_id(self):
        self.assertEquals(self.lab.getID(), 1011, "getID() did not retrieve correct section_id")


class TestSectionGetParentCourse(TestCase):  # Joe
    lab = None
    course = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        self.course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )

        tmp_lab = Lab.objects.create(
            section=tmp_section,
            ta=tmp_ta
        )

        self.lab = LabObj(tmp_lab)

    def test_get_parent_course(self):
        self.assertEquals(self.lab.getParentCourse(), self.course,
                          "getParentCourse() did not retrieve correct course")
