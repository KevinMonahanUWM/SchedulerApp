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
        ses["user"] = self.admin_user.__str__()
        ses.save()

        # Create an initial course
        self.course = Course.objects.create(course_id=101, semester='Fall 2023', name='Introduction to Testing',
                                            description='A course about writing tests in Django.', num_of_sections=3,
                                            modality='Online')
        ses["course_id"] = self.course.course_id
        ses.save()

    def test_edit_course_success(self):
        updated_data = {
            'semester': 'Spring 2024',
            'name': 'Advanced Testing',
            'description': 'An advanced course on testing practices.',
            'num_of_sections': 2,
            'modality': 'Hybrid'
        }
        response = self.client.post('/home/managecourse/edit/', updated_data)


        self.course = Course.objects.get(course_id=101)
        self.assertEqual(self.course.semester, updated_data['semester'])
        self.assertEqual(self.course.name, updated_data['name'])
        self.assertEqual(self.course.description, updated_data['description'])
        self.assertEqual(self.course.num_of_sections, updated_data['num_of_sections'])
        self.assertEqual(self.course.modality, updated_data['modality'])

    def test_edit_course_invalid_input(self):
        response = self.client.post('/home/managecourse/edit/', {
            'semester': 'Spring 2024',
            'name': '',  # Invalid input
            'description': 'A course on testing practices.',
            'num_of_sections': 2,
            'modality': 'Hybrid',
        })

        self.course.refresh_from_db()
        self.assertNotEqual(self.course.name, '')

    def test_discard_course_changes(self):
        original_data = {
            'semester': self.course.semester,
            'name': self.course.name,
            'description': self.course.description,
            'num_of_sections': self.course.num_of_sections,
            'modality': self.course.modality
        }
        response = self.client.post('/home/managecourse/edit/', original_data)

        self.course.refresh_from_db()

        self.assertEqual(self.course.name, original_data['name'])
