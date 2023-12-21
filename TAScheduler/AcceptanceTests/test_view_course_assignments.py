from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, Instructor, Course
class TestViewCourseAssignments(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a user using the custom User model fields.
        self.user = User.objects.create(
            email_address='instructor@example.com',
            password='password',  # Normally, you'd hash this password
            first_name='Instructor',
            last_name='User',
            home_address='123 Test St',
            phone_number=1234567890
        )

        # Create an Instructor instance associated with the user.
        self.instructor = Instructor.objects.create(user=self.user)
        ses = self.client.session
        ses["user"] = str(self.instructor)
        ses.save()
        # Create a course.
        self.course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Test Course',
            description='A course for testing',
            num_of_sections=1,
            modality='Online'
        )

        # Log in using the email_address.
        # Adjust if your project uses a different authentication method.
        self.client.login(email_address='instructor@example.com', password='password')


    def test_instructor_can_view_assignments(self):

        response = self.client.post("/home/managecourse/", {'course': self.course, 'details': "Detail"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.course.name)
        self.assertContains(response, self.course.course_id)
