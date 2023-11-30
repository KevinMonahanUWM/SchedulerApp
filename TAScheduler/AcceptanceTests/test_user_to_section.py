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
        ses["user"] = self.account.str()  # should be done at login
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

        self.user.get("/home/managecourse/adduser/", {"user", self.ta}, follow=True)
        response = self.user.post("home/managesection/adduser/choosesection/", {"course", self.section},
                                  follow=True)
        self.assertEquals(TAObj(tmp_ta).getTALabAsgmts(), tmp_lab, "TA to lab link was not made")
        self.assertRedirects(response, '/home/success/')

    def test_ta_to_lec(self):
        tmp_lec = Lecture.objects.create(
            section=self.section,
            ta=self.ta,
            instructor=self.instructor
        )
        tmp_lec.save()

    def test_instructor_to_lec(self):
        tmp_lec = Lecture.objects.create(
            section=self.section,
            ta=self.ta,
            instructor=self.instructor
        )
        tmp_lec.save()
