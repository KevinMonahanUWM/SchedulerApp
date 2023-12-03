from django.test import TestCase, Client

from TAScheduler.models import User, Instructor, Course, InstructorToCourse, Administrator


class SuccessfulCreation(TestCase):
    user = None
    instructor = None
    course = None
    instructorToCourse = None

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
        response = self.user.post("/home/managecourse/addinstructor/", {"chosen": self.instructor}, follow=True)
        self.assertEquals(response.context["user"], "Success", "Instructor to Course was not made")
        response = self.user.post("/home/managecourse/addinstructor/choosecourse/",
                                  {"chosen": self.instructor, "course": self.course},
                                  follow=True)
        self.assertEquals(response.context["message"], "Success", "Instructor to Course was not made")
        self.assertTrue(InstructorToCourse.objects.filter(instructor=self.instructor, course=self.course).exists(),
                        "Instructor to Course link was not made")

    def test_successful_instructor_to_course_creation(self):
        # Simulate successful creation of an InstructorToCourse object
        response = self.client.post('/home/managecourse/addinstructor/', {'user': self.instructor})

        # Assert that the response is a success (HTTP 200 OK) and check if the expected InstructorToCourse object exists
        self.assertEqual(response.status_code, 200)
        self.assertTrue(InstructorToCourse.objects.filter(instructor=self.instructor).exists())


class NoInstructor(TestCase):
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

    def test_no_instructor(self):
        resp = self.user.get("/home/managecourse/addinstructor", follow=True)
        self.assertEquals(len(Instructor.objects.filter()), 0, "Cannot assign instructor when none exist")


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
        resp = self.user.post("/home/managecourse/addinstructor/", {"user": self.instructor}, follow=True)
        self.assertEquals(resp.context["message"], "Error: No Courses to display",
                          "Cannot assign courses when none exist")


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
        resp = self.user.post("/home/managecourse/addinstructor", {"user": str(self.instructor)}, follow=True)
        print(resp.context)
        self.assertEquals(resp.context["message"], "Instructor has max assignments",
                          "Cannot assign courses when instructor is at max")


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
        resp = self.user.post("/home/managecourse/addinstructor", {"selection": self.instructor}, follow=True)
        self.assertEquals(resp.context["instructor"], self.instructor, "Instructor not transferred over properly")
