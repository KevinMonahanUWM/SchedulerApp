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
        ses["user"] = self.admin_user.__str__()
        ses.save()

        # Create an initial course
        self.course = Course.objects.create(course_id=101, semester='Fall 2023', name='Introduction to Testing',
                                            description='A course about writing tests in Django.', num_of_sections=3,
                                            modality='Online')

    def test_delete_course_success(self):
        self.client.login(email_address=self.admin_user.user.email_address, password='password')
        response = self.client.post('/home/managecourse/', {'course_id': self.course.course_id, 'edit': 'Edit'})
        qs = Course.objects.filter(pk=self.course.pk)
        self.assertFalse(qs.exists())


