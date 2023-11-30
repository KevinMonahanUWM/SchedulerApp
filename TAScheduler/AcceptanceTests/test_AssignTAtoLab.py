from django.test import TestCase, Client

from TAScheduler.models import User, TA, Course, TAToCourse, Administrator


class SuccessfulCreation(TestCase):
    user = None
    ta = None
    course = None
    TAToCourse = None

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
        ses["user"] = self.account.str()  # should be done at login
        ses.save()
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online", credits=3)
        self.course.save()

        self.TAToCourse = TAToCourse.objects.create(ta=self.ta, course=self.course)
        self.TAToCourse.save()

    def test_creation(self):
        # I think that TA to course would also be in course management which is why URL is such

        self.user.post("/home/managecourse/addta", {"selection", self.ta}, follow=True)
        response = self.user.post("/home/managecourse/addta/course-select", {"selection", self.course},
                                  follow=True)
        self.assertEquals(self.ta, User.objects.get(self.ta), "TA to course link was not made")
        self.assertRedirects(response, '/home/managecourse/addta/course-select/success')


class NoTA(TestCase):
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

    def test_no_ta(self):
        response = self.user.get("/home/managecourse/addta")
        self.assertEquals(response.context["message"], "No existing TA's to assign")


class NoCourse(TestCase):
    user = None
    ta = None

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
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

    def test_no_course(self):
        response = self.user.post("/home/managecourse/addta", {"selection", self.ta}, follow=True)
        self.assertEquals(response.context["message"], "No existing courses to assign")


class TANoRoom(TestCase):
    user = None
    ta = None

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
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

    def test_ta_no_room(self):
        resp = self.user.post("/home/managecourse/addta", {"selection", self.ta}, follow=True)
        self.assertEquals(resp.context["message"], "TA has max assignments",
                          "Cannot assign courses when TA is at max")


class SuccessfulTransfer(TestCase):
    user = None
    ta = None

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
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

    def test_ta_to_next(self):
        resp = self.user.post("/home/managecourse/addta", {"selection", self.ta}, follow=True)
        self.assertEquals(resp.context["ta"], self.ta, "TA not transferred over properly")

    """                             I don't think this needs this but just in case, also I just thought that it probably
     doesn't after I finished it
class CourseHasTA(TestCase):
    user = None
    ta = None
    ta2 = None
    course = None
    taToCourse = None

    def setUp(self):
        self.user = Client()
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        temp2 = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp2.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        self.ta2 = TA.objects.create(user=temp2)
        self.ta2.save()

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online", credits=3)
        self.course.save()

        self.TAToCourse = TAToCourse.objects.create(ta=self.ta, course=self.course)
        self.TAToCourse.save()

    def test_course_full(self):
        self.user.post("/home/managecourse/addta", {"selection", self.ta}, follow=True)
        response = self.user.post("/home/managecourse/addta/course-select", {"selection", self.course},
                                  follow=True)

        self.user.post("/home/managecourse/addta", {"selection", self.ta2}, follow=True)
        response2 = self.user.post("/home/managecourse/addta/course-select", {"selection", self.course},
                                  follow=True)

        self.assertEquals(response.context["message"], "Course already has TA assigned", "TA assigned to full course")
    """
