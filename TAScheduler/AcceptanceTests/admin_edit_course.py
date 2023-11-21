from django.test import TestCase
from django.urls import reverse
from TAScheduler.models import Course, User, Administrator

class AdminEditCourseTestCase(TestCase):
    def setUp(self):
        # Create a course for editing
        self.course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Intro to Testing',
            description='A course on testing practices.',
            num_of_sections=1,
            modality='Online',
            credits=3
        )
        # Create an admin user and log them in
        admin_user = User.objects.create(email_address='admin@example.com', password='password')
        Administrator.objects.create(user=admin_user)
        self.client.login(email_address=admin_user.email_address, password='password')

    def test_edit_course_success(self):
        # Admin logs in and edits a course successfully
        updated_data = {
            'course_id': self.course.course_id,
            'semester': 'Spring 2024',
            'name': 'Advanced Testing',
            'description': 'An advanced course on testing practices.',
            'num_of_sections': 2,
            'modality': 'Hybrid',
            'credits': 4
        }
        response = self.client.post(reverse('edit_course', args=[self.course.pk]), updated_data)
        self.assertRedirects(response, reverse('course_management'))

        self.course.refresh_from_db()
        self.assertEqual(self.course.semester, updated_data['semester'])
        self.assertEqual(self.course.name, updated_data['name'])
        self.assertEqual(self.course.description, updated_data['description'])
        self.assertEqual(self.course.num_of_sections, updated_data['num_of_sections'])
        self.assertEqual(self.course.modality, updated_data['modality'])
        self.assertEqual(self.course.credits, updated_data['credits'])

    def test_edit_course_invalid_input(self):
        # Admin attempts to update a course with invalid input
        response = self.client.post(reverse('edit_course', args=[self.course.pk]), {
            'course_id': self.course.course_id,
            'semester': 'Spring 2024',
            'name': '',  # Invalid input
            'description': 'A course on testing practices.',
            'num_of_sections': 2,
            'modality': 'Hybrid',
            'credits': 4
        })
        self.assertEqual(response.status_code, 200)  # The page is re-rendered
        self.assertFormError(response, 'form', 'name', 'This field cannot be blank.')
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.name, '')  # The name should remain unchanged

    def test_discard_course_changes(self):
        # Admin attempts to make changes but then discards them
        original_name = self.course.name
        response = self.client.post(reverse('course_edit', args=[self.course.pk]))
        self.assertRedirects(response, reverse('course_management'))
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, original_name)