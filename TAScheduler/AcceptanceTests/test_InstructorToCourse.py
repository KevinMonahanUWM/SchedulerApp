from django.test import TestCase, Client
from django.utils.datastructures import MultiValueDictKeyError

from TAScheduler.models import User, Instructor, Course, InstructorToCourse, Administrator


class SuccessfulCreation(TestCase):
    user = None
    instructor = None
    course = None

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
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp)
        self.instructor.save()

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online")
        self.course.save()


    # /home/managecourse/addinstructor
    def test_creation(self):
        response = self.user.post("/home/managecourse/addinstructor/", {"user": self.instructor, "course": self.course}, follow=True)
        self.assertIsNotNone(InstructorToCourse.objects.get(instructor=self.instructor, course=self.course))

class NoInstructor(TestCase):
    user = None
    course = None

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

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online")
        self.course.save()

    def test_no_instructor(self):
        response = self.user.post("/home/managecourse/addinstructor/", {"course": self.course})
        self.assertEquals(
            response.context["message"],
            "Please select an instructor",
            "Did not display error when no instructor selected"
        )

class NoCourse(TestCase):
    user = None
    instructor = None

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

        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp)
        self.instructor.save()

    def test_no_course(self):
        response = self.user.post("/home/managecourse/addinstructor/", {"user": self.instructor})
        self.assertEquals(
            response.context["message"],
            "Please select a course",
            "Did not display error when no instructor selected"
        )


class InstructorNoRoom(TestCase):
    user = None
    instructor = None

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
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp, max_assignments=0)
        self.instructor.save()

    def test_instructor_no_room(self):
        pass


class SuccessfulTransfer(TestCase):
    user = None
    instructor = None

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

        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp)
        self.instructor.save()

    def test_instructor_to_next(self):
        pass
