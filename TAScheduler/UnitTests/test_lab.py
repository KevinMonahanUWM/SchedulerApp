from django.test import TestCase
from TAScheduler.models import User, Course, TA, Section, Lab
from TAScheduler.views_methods import LabObj


class TestLabInit(TestCase):
    lab = None
    info = None
    tempLab = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@test.com",
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

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        self.tmp_lab = Lab.objects.create(
            section=tmp_section,
            ta=tmp_ta
        )

        self.lab = LabObj(self.tmp_lab)

    def test_lab_make(self):
        self.assertIsNotNone(self.lab, "__init__ failed in making Lab")

    def test_bad_lab_make(self):
        with self.assertRaises(TypeError, msg="__init__ failed in making Lab, bad input"):
            LabObj(5)


class TestLabGetLabTAAssignment(TestCase):  # Joe
    lab = None
    ta = None

    # noinspection DuplicatedCode
    def setUp(self):
        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )

        self.lab = Lab.objects.create(
            section=tmp_section
        )

    def test_get_ta(self):
        temp = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp.save()
        self.ta = TA.objects.create(user=temp, grader_status=True)
        self.ta.save()

        self.lab.ta = self.ta
        self.lab.save()

        self.labObj = LabObj(self.lab)  # Form lab after adding TA manually

        self.assertEqual(
            self.ta,
            self.labObj.getLabTAAsgmt(),
            "getLabTAAssignment() does not retrieve correct ta; Test may also be accepting wrong object")

    def test_get_but_no_ta(self):
        self.labObj = LabObj(self.lab)  # Form lab with no TA

        self.assertIsNone(self.labObj.getLabTAAsgmt(), "getLabTAAssignment() finds something with no TA")


class TestLabAddTA(TestCase):  # Joe
    lab = None
    ta = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        self.ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        self.ta.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lab = Lab.objects.create(
            section=tmp_section,
        )
        tmp_lab.save()

        self.lab = LabObj(tmp_lab)

    def test_add_ta(self):
        self.lab.addTA(self.ta)
        # Gives error for TAObj having no 'user' but I think that's because __init__ not implemented in my branch
        self.assertEqual(self.ta, self.lab.getLabTAAsgmt(),
                         "addTA() does not add TA to lab")

    def test_add_ta_but_full(self):
        temp2 = User(email_address="test2@test.com", password="password2", first_name="first2", last_name="last2",
                     home_address="Your mom's house", phone_number=1234567890)
        temp2.save()
        temp_ta = TA.objects.create(user=temp2, grader_status=True)
        self.lab.addTA(self.ta)
        # Gives error for TAObj having no 'user' but I think that's because __init__ not implemented in my branch
        with self.assertRaises(RuntimeError, msg="Tried to add TA to full Lab"):
            self.lab.addTA(temp_ta)


class TestLabRemoveTA(TestCase):  # Joe
    lab = None
    ta = None

    def setUp(self):
        temp_user = User(
            email_address="test@test.com",
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

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lab = Lab.objects.create(
            section=tmp_section,
            ta=tmp_ta
        )

        self.lab = LabObj(tmp_lab)

    def test_remove(self):
        self.lab.removeTA()
        self.assertIsNone(self.lab.getLabTAAsgmt(), "removeTA() does not remove TA from lab")

    def test_none_to_remove(self):
        self.lab.removeTA()
        with self.assertRaises(RuntimeError, msg="Tried to remove TA when none in lab"):
            self.lab.removeTA()
