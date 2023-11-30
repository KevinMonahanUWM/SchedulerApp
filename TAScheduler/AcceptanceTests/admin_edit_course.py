from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import Course, User, Administrator

email_address = None
password = None
course_id = None
name = None
semester = None
num_of_sections = None
modality = None


class AdminEditCourseTestCase(TestCase):
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

    def test_edit_course_success(self):
        updated_data = {
            'course_id': self.course.course_id,
            'semester': 'Spring 2024',
            'name': 'Advanced Testing',
            'description': 'An advanced course on testing practices.',
            'num_of_sections': 2,
            'modality': 'Hybrid',
            'credits': 4
        }
        response = self.client.post('/home/managecourse/edit', updated_data)
        self.assertRedirects(response, '/home/success')

        self.course.refresh_from_db()
        self.assertEqual(self.course.semester, updated_data['semester'])
        self.assertEqual(self.course.name, updated_data['name'])
        self.assertEqual(self.course.description, updated_data['description'])
        self.assertEqual(self.course.num_of_sections, updated_data['num_of_sections'])
        self.assertEqual(self.course.modality, updated_data['modality'])
        self.assertEqual(self.course.credits, updated_data['credits'])

    def test_edit_course_invalid_input(self):
        response = self.client.post('/home/managecourse/edit', {
            'course_id': self.course.course_id,
            'semester': 'Spring 2024',
            'name': '',  # Invalid input
            'description': 'A course on testing practices.',
            'num_of_sections': 2,
            'modality': 'Hybrid',
            'credits': 4
        })
        self.assertEqual(response.status_code, 200)

        self.course.refresh_from_db()
        self.assertNotEqual(self.course.name, '')

    def test_discard_course_changes(self):
        original_name = self.course.name
        response = self.client.post('/home/managecourse/edit')
        self.assertRedirects(response, '/home/managecourse')

        self.course.refresh_from_db()
        self.assertEqual(self.course.name, original_name)