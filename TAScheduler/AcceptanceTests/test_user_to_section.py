from django.db.models import QuerySet
from django.test import TestCase, Client

from TAScheduler.models import User, Instructor, Course, TA, Section, Lecture, Lab, Administrator
from TAScheduler.views_methods import TAObj


class SuccessfulCreation(TestCase):
    ta = None
    instructor = None
    section = None
    user = None

    def setUp(self):
        self.user = Client()
        self.account = Administrator.objects.create(
            user=User.objects.create(
                email_address="test@uwm.edu",
                password="pass",
                first_name="test",
                last_name="test",
                home_address="home",
                phone_number=1234567890
            )
        )
        ses = self.client.session
        ses["user"] = self.account.__str__()  # should be done at login
        ses.save()

        temp_user = User(
            email_address="test@ta.com",
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

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        self.instructor = Instructor.objects.create(
            user=temp_user2
        )
        self.instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmp_course.save()

        self.section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        self.section.save()

    def test_ta_to_lab(self):
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
            grader_status=False
        )
        tmp_ta.save()

        tmp_lab = Lab.objects.create(
            section=self.section,
            ta=tmp_ta
        )
        tmp_lab.save()

        self.user.post("/home/managecourse/adduser/", {"user": str(self.ta)}, follow=True)
        response = self.user.post("/home/managesection/adduser/choosesection/", {"course": self.section})
        self.assertEqual(TAObj(tmp_ta).getTALabAsgmts().first(), tmp_lab, "TA to lab link was not made")

    def test_ta_to_lec(self):
        tmp_lec = Lecture.objects.create(
            section=self.section,
            ta=self.ta,
            instructor=self.instructor
        )
        tmp_lec.save()
        self.user.post("/home/managecourse/adduser/", {"user": str(self.ta)}, follow=True)
        response = self.user.post("/home/managesection/adduser/choosesection/", {"course": self.section})
        self.assertEqual(TAObj(self.ta).getTALabAsgmts().first(), tmp_lec, "TA to lab link was not made")

    def test_instructor_to_lec(self):
        tmp_lec = Lecture.objects.create(
            section=self.section,
            ta=self.ta,
            instructor=self.instructor
        )
        tmp_lec.save()


class NoUsers(TestCase):
    section = None
    user = None

    def setUp(self):
        self.user = Client()
        self.account = Administrator.objects.create(
            user=User.objects.create(
                email_address="test@uwm.edu",
                password="pass",
                first_name="test",
                last_name="test",
                home_address="home",
                phone_number=1234567890
            )
        )
        ses = self.client.session
        ses["user"] = self.account.__str__()  # should be done at login
        ses.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmp_course.save()

        self.section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        self.section.save()

    def test_no_users(self):
        pass


class NoSections(TestCase):
    ta = None
    instructor = None
    section = None
    user = None

    def setUp(self):
        self.user = Client()
        self.account = Administrator.objects.create(
            user=User.objects.create(
                email_address="test@uwm.edu",
                password="pass",
                first_name="test",
                last_name="test",
                home_address="home",
                phone_number=1234567890
            )
        )
        ses = self.client.session
        ses["user"] = self.account.__str__()  # should be done at login
        ses.save()

        temp_user = User(
            email_address="test@ta.com",
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

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        self.instructor = Instructor.objects.create(
            user=temp_user2
        )
        self.instructor.save()

    def test_no_courses(self):
        pass


class FullSections(TestCase):
    taT = None
    taF = None
    instructor = None
    section = None
    user = None
    lab = None
    lecture = None

    def setUp(self):
        self.user = Client()
        self.account = Administrator.objects.create(
            user=User.objects.create(
                email_address="test@uwm.edu",
                password="pass",
                first_name="test",
                last_name="test",
                home_address="home",
                phone_number=1234567890
            )
        )
        ses = self.client.session
        ses["user"] = self.account.__str__()  # should be done at login
        ses.save()

        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        self.taT = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        self.taT.save()

        temp_user = User(
            email_address="test2@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        self.taF = TA.objects.create(
            user=temp_user,
            grader_status=False
        )
        self.taF.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        self.instructor = Instructor.objects.create(
            user=temp_user2
        )
        self.instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmp_course.save()

        self.section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        self.section.save()

        self.lab = Lab.objects.create(
            section=self.section,
            ta=self.taF
        )

        self.lecture = Lecture.objects.create(
            section=self.section,
            ta=self.taT,
            instructor=self.instructor
        )

    def test_add_full_instr(self):
        pass

    def test_add_ta_full_lab(self):
        pass

    def test_add_ta_full_lec(self):
        pass
