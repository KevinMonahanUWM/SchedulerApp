from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import Course, Section, User, TA, InstructorToCourse

email_address = None
password = None
course_id = None
name = None
semester = None
num_of_sections = None
modality = None


class AdminDeleteCourseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an admin user and course for testing
        self.admin_user = User.objects.create(email_address='admin@example.com', password='password')
        self.course = Course.objects.create(course_id=1, name='Test Course', semester='Fall', num_of_sections=1,
                                            modality='Online', credits=3)

    def test_delete_course_success(self):
        self.client.login(email_address=self.admin_user.email_address, password='password')

        # Attempt to delete the course
        response = self.client.post(reverse('delete_course'), {'course_id': self.course.course_id})
        self.assertRedirects(response, reverse('course_management'))
        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())

    def test_delete_course_no_courses_available(self):
        # Make sure no courses are present
        Course.objects.all().delete()

        self.client.login(email_address=self.admin_user.email_address, password='password')

        # Attempt to access the delete course page
        response = self.client.get(reverse('delete_course'))
        self.assertIn('No Courses to Delete', response.content.decode())
        self.assertEqual(response.context["message"], "Successfully deleted course")