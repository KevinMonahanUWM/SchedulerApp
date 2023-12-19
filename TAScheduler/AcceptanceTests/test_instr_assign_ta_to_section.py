import datetime

from django.test import TestCase, Client

from TAScheduler.models import User, Instructor, Course, InstructorToCourse, Administrator, Lab, Section, Lecture
from TAScheduler.views_methods import InstructorObj


class SuccessfulCreation(TestCase):
    user = None
    instructor = None
    ta = None
    lab = None
    lec = None

    # noinspection DuplicatedCode
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
        self.ta = User(email_address="ta@ta.com", password="password", first_name="first", last_name="last",
                       home_address="Your mom's house", phone_number=1234567890)
        self.ta.save()

        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp)
        self.instructor = InstructorObj(self.instructor)

        tempcourse = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                           num_of_sections=3, modality="online")
        tempcourse.save()

        tempsection = Section.objects.create(section_id=800, course=tempcourse, location="Behind you",
                                             meeting_time=datetime.datetime(2023, 12, 19, 15, 30, 0))
        tempsection.save()

        self.lab = Lab.objects.create(section=tempsection)
        self.lec = Lecture.objects.create(section=tempsection)

    def test_success_instr_assign_lab(self):
        resp = self.client.post("url here", data=self.lecInfo)
    def test_success_instr_assign_lec(self):
