from django.test import TestCase, Client

from TAScheduler.models import User, TA, Course, TAToCourse, Administrator


class SuccessfulCreation(TestCase):
    user = None
    TA = None
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

        self.TA = TA.objects.create(user=temp, grader_status=True)
        self.TA.save()

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online")
        self.course.save()

    def test_creation(self):
        self.user.post("/home/managecourse/addta/", {"user": self.TA, "course": self.course},
                       follow=True)
        self.assertIsNotNone(TAToCourse.objects.get(ta=self.TA, course=self.course))


class NoTA(TestCase):
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

    def test_no_TA(self):
        response = self.user.post("/home/managecourse/addta/", {"course": self.course})
        self.assertEquals(
            response.context["message"],
            "Please select a ta",
            "Did not display error when no TA selected"
        )


class NoCourse(TestCase):
    user = None
    TA = None

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

        self.TA = TA.objects.create(user=temp, grader_status=True)
        self.TA.save()

    def test_no_course(self):
        response = self.user.post("/home/managecourse/addta/", {"user": self.TA})
        self.assertEquals(
            response.context["message"],
            "Please select a course",
            "Did not display error when no TA selected"
        )


class TANoRoom(TestCase):
    user = None
    TA = None

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

        self.TA = TA.objects.create(user=temp, grader_status=True, max_assignments=0)
        self.TA.save()

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online")
        self.course.save()

    def test_TA_no_room(self):
        response = self.user.post("/home/managecourse/addta/", {"user": self.TA, "course": self.course},
                                  follow=True)
        self.assertEquals(response.context["message"],
                          "Can't assign a course past a TA's maximum capacity",
                          "Doesn't raise error when TA at max"
                          )


class CourseNoRoom(TestCase):
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
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.TA = TA.objects.create(user=temp, grader_status=True)
        self.TA.save()

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=0, modality="online")
        self.course.save()

    def test_course_no_room(self):
        response = self.user.post("/home/managecourse/addta/", {"user": self.TA, "course": self.course},
                                  follow=True)
        self.assertEquals(response.context["message"],
                          "Can't assign course that has reached it's maximum assignments",
                          "Doesn't raise error when Course at max"
                          )
