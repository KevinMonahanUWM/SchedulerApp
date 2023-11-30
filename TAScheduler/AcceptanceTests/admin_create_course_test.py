from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import User, Course, Instructor, TA, Administrator


class AdminCreateCourseTestCase(TestCase):
    admin_user = None
    course = None
    password = None
    first_name = None
    last_name = None
    home_address = None
    phone_number = None
    course_id = None
    semester = None
    name = None
    description = None
    num_of_sections = None
    modality = None
    credits = None

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
        Course.objects.create(course_id=101, semester='Fall 2023', name='Introduction to Testing',
                              description='A course about writing tests in Django.', num_of_sections=3,
                              modality='Online', credits=4)

    def test_create_course_success(self):
        response = self.client.post('/home/managecourse/create', {
            'course_id': 102,
            'semester': 'Fall 2023',
            'name': 'Advanced Testing',
            'description': 'An advanced course about writing tests in Django.',
            'num_of_sections': 3,
            'modality': 'Online',
            'credits': 4
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(course_id=102).exists())

    def test_create_course_duplicate(self):
        response = self.client.post('/home/managecourse/create', {
            'course_id': 101,
            'semester': 'Spring 2024',
            'name': 'Advanced Testing',
            'description': 'An advanced course about writing tests in Django.',
            'num_of_sections': 3,
            'modality': 'In-person',
            'credits': 4
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('A course with this ID already exists', response.content.decode())
        self.assertEqual(Course.objects.filter(course_id=101).count(), 1)