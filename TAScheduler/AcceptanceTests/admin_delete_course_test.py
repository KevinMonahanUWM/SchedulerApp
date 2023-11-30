from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import Course, Section, User, TA, InstructorToCourse, Administrator


class AdminDeleteCourseTestCase(TestCase):
    email_address = None
    password = None
    course_id = None
    name = None
    semester = None
    num_of_sections = None
    modality = None

    def setUp(self):
        self.client = Client()
        self.admin_user = Administrator.objects.create(
            user=User.objects.create(email_address="admin@example.com", password="adminpassword",
                                     first_name="Admin", last_name="User", home_address="123 Admin St",
                                     phone_number="1234567890")
        )
        ses = self.client.session
        ses["user"] = "admin@example.com"
        ses.save()

        # Create an initial course
        self.course = Course.objects.create(course_id=101, semester='Fall 2023', name='Introduction to Testing',
                                            description='A course about writing tests in Django.', num_of_sections=3,
                                            modality='Online', credits=4)

    def test_delete_course_success(self):
        self.client.login(email_address=self.admin_user.user.email_address, password='password')

        # Attempt to delete the course
        response = self.client.post('home/manageaccount/delete', {'course_id': self.course.course_id})
        self.assertRedirects(response, 'home/managecourse')
        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())

    def test_delete_course_no_courses_available(self):
        # Make sure no courses are present
        Course.objects.all().delete()

        self.client.login(email_address=self.admin_user.user.email_address, password='password')

        # Attempt to access the delete course page
        response = self.client.get('home/managecourse/delete')
        self.assertIn('No Courses to Delete', response.content.decode())
        self.assertEqual(response.context["message"], "Successfully deleted course")
