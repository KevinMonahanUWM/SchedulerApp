from datetime import datetime
from django.test import TestCase
from TAScheduler.models import Lab, Lecture, User, TA, Course, Administrator, Section
from TAScheduler.views_methods import LabObj, LectureObj, AdminObj


class TestSecTAAsgmt(TestCase):
    admin = None
    ta = None
    section = None

    def setUp(self):
        hold_user = User(
            email_address='admin@example.com',
            password='admin_password',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number=1234567890
        )
        hold_user.save()
        hold_admin = Administrator(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

        tempcourse = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online'
        )
        tempcourse.save()

        self.section = Section.objects.create(
            section_id=800,
            course=tempcourse,
            location="East Lane",
            meeting_time=datetime(2023, 1, 1, 12, 0, 0)
        )
        self.section.save()

        tmpuser = User.objects.create(
            email_address='ta@example.com',
            password='password',
            first_name='Ta',
            last_name='User',
            home_address='123 TA St',
            phone_number=1234567890
        )
        self.ta = TA.objects.create(
            user=tmpuser,
            grader_status=False
        )

    def test_success_lab(self):
        laboratory = Lab.objects.create(
            section=self.section
        )
        labobj = LabObj(laboratory)
        self.admin.sectionTAAsmgt(self.ta, labobj)
        self.assertEqual(labobj.getLabTAAsgmt(), self.ta, "Did not assign correct laboratory")

    def test_success_lec(self):
        lecture = Lecture.objects.create(
            section=self.section
        )
        lecobj = LectureObj(lecture)
        tmpuser = User.objects.create(
            email_address='ta@example.com',
            password='password',
            first_name='Ta',
            last_name='User',
            home_address='123 TA St',
            phone_number=1234567890
        )
        tmpta = TA.objects.create(
            user=tmpuser,
            grader_status=True
        )
        tmpta.save()
        self.admin.sectionTAAsmgt(tmpta, lecobj)
        self.assertEqual(lecobj.getLectureTAAsgmt(), tmpta, "Did not assign correct lecture")

    def test_bad_ta(self):
        laboratory = Lab.objects.create(
            section=self.section
        )
        labobj = LabObj(laboratory)
        with self.assertRaises(TypeError, msg="Does not raise typerror for bad TA"):
            self.admin.sectionTAAsmgt("String!", labobj)

    def test_bad_section(self):
        with self.assertRaises(TypeError, msg="Does not raise typerror for bad Section"):
            self.admin.sectionTAAsmgt(self.ta, "STRING!")

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
        self.assertEqual(self.lab.getID(), 1011, "getID() did not retrieve correct section_id")


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
        self.assertEqual(self.lab.getParentCourse(), self.course,
                          "getParentCourse() did not retrieve correct course")