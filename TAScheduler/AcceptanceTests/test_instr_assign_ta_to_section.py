import datetime

from django.test import TestCase, Client

from TAScheduler.models import User, TA, Course, TAToCourse, Instructor, Section, Lab, Lecture


class SuccessfulCreation(TestCase):
    user = None
    TA = None
    course = None
    section = None
    lab = None
    lec = None

    # noinspection DuplicatedCode
    def setUp(self):
        self.user = Client()
        self.account = Instructor.objects.create(
            user=User.objects.create(
                email_address="test@uwm.edu",
                password="pass",
                first_name="test",
                last_name="test",
                home_address="home",
                phone_number=1234567890
            )
        )
        ses = self.user.session
        ses["user"] = self.account.__str__()  # should be done at login
        ses.save()
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.TA = TA.objects.create(user=temp, grader_status=True)
        self.TA.save()

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online")
        self.course.save()
        TAToCourse.objects.create(ta=self.TA, course=self.course)

        self.section = Section.objects.create(section_id=800, course=self.course, location="Maybe",
                                              meeting_time=datetime.datetime(2023, 12, 19, 15, 30, 0))

        self.lab = Lab.objects.create(section=self.section)
        self.lab.save()
        self.lec = Lecture.objects.create(section=self.section)
        self.lec.save()

    def test_success_lab(self):
        temp = User(email_address="test1@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()
        tempta = TA.objects.create(user=temp, grader_status=False)
        tempta.save()
        self.user.post("/home/managesection/assignuser/",
                       {"section": self.lab, "user": tempta, "assign": "Assign"})
        lab = Lab.objects.get(section=self.lab.section)
        self.assertEquals(lab.ta, tempta, "Did not assign TA to lab properly")

    def test_success_lec(self):
        self.user.post("/home/managesection/assignuser/",
                       {"section": self.lec, "user": self.TA})
        lec = Lecture.objects.get(section=self.lec.section)
        self.assertEquals(lec.ta, self.TA, "Did not assign TA to lec properly")

    def test_self_success_lec(self):
        self.user.post("/home/managesection/assignuser/",
                       {"section": self.lec, "user": self.account})
        lec = Lecture.objects.get(section=self.lec.section)
        self.assertEquals(lec.instructor, self.account, "Did not assign TA to lec properly")

class MissingCourseOrUser(TestCase):
    user = None
    TA = None
    section = None
    lab = None
    lec = None

    # noinspection DuplicatedCode
    def setUp(self):
        self.user = Client()
        self.account = Instructor.objects.create(
            user=User.objects.create(
                email_address="test@uwm.edu",
                password="pass",
                first_name="test",
                last_name="test",
                home_address="home",
                phone_number=1234567890
            )
        )
        ses = self.user.session
        ses["user"] = self.account.__str__()  # should be done at login
        ses.save()
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.TA = TA.objects.create(user=temp, grader_status=True)
        self.TA.save()

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online")
        self.course.save()
        TAToCourse.objects.create(ta=self.TA, course=self.course)

        self.section = Section.objects.create(section_id=800, course=self.course, location="Maybe",
                                              meeting_time=datetime.datetime(2023, 12, 19, 15, 30, 0))

        self.lab = Lab.objects.create(section=self.section)
        self.lab.save()
        self.lec = Lecture.objects.create(section=self.section)
        self.lec.save()

    def test_no_users(self):
        with self.assertRaises(Exception):
            self.user.post("/home/managesection/assignuser/", {"user": "","section": self.lec})

    def test_no_sections(self):
        with self.assertRaises(Exception):
            self.user.post("/home/managesection/assignuser/", {"user": "", "section": ""})
