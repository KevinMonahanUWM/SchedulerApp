from django.test import TestCase, Client

from TAScheduler.models import User, Instructor, Course, InstructorToCourse


class SuccessfulCreation(TestCase):
    user = None
    instructor = None
    course = None
    instructorToCourse = None

    # noinspection DuplicatedCode
    def setUp(self):
        self.user = Client()
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp)
        self.instructor.save()

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online", credits=3)
        self.course.save()

        self.instructorToCourse = InstructorToCourse.objects.create(instructor=self.instructor, course=self.course)

    # /home/managecourse/addinstructor
    def test_creation(self):
        self.user.post("/home/managecourse/addinstructor", {"selection", self.instructor}, follow=True)
        response = self.user.post("/home/managecourse/addinstructor/course-select", {"selection", self.course},
                                  follow=True)
        self.assertEquals(self.instructorToCourse, User.objects.get(self.instructorToCourse),
                          "Instructor to Course link was not made")
        self.assertRedirects(response, '/home/managecourse/addinstructor/course-select/success')


class NoInstructor(TestCase):
    user = None

    def setUp(self):
        self.user = Client()

    def test_no_instructor(self):
        resp = self.user.get("/home/managecourse/addinstructor")
        self.assertEquals(resp.context["message"], "No Existing Instructors to Assign",
                          "Cannot assign instructor when none exist")


class NoCourse(TestCase):
    user = None
    instructor = None

    def setUp(self):
        self.user = Client()

        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp)
        self.instructor.save()

    def test_no_course(self):
        resp = self.user.post("/home/managecourse/addinstructor", {"selection", self.instructor}, follow=True)
        self.assertEquals(resp.context["message"], "No existing Courses to assign",
                          "Cannot assign courses when none exist")


class InstructorNoRoom(TestCase):
    user = None
    instructor = None

    def setUp(self):
        self.user = Client()
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp, max_assignments=0)
        self.instructor.save()

    def test_instructor_no_room(self):
        resp = self.user.post("/home/managecourse/addinstructor", {"selection", self.instructor}, follow=True)
        self.assertEquals(resp.context["message"], "Instructor has max assignments",
                          "Cannot assign courses when instructor is at max")


class SuccessfulTransfer(TestCase):
    user = None
    instructor = None

    def setUp(self):
        self.user = Client()
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp)
        self.instructor.save()

    def test_instructor_to_next(self):
        resp = self.user.post("/home/managecourse/addinstructor", {"selection", self.instructor}, follow=True)
        self.assertEquals(resp.context["instructor"], self.instructor, "Instructor not transferred over properly")
