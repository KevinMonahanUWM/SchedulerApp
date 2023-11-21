from django.test import TestCase
from django.urls import reverse
from TAScheduler.models import User, Course, Instructor, TA, Administrator


class AdminCreateCourseTestCase(TestCase):
    def setUp(self):
        # Create an admin user for login
        admin_user = User.objects.create(
            email_address='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        Administrator.objects.create(user=admin_user)
        self.client.login(email_address=admin_user.email_address,
                          password='adminpassword')  # Update as per your login logic

    def test_create_course_success(self):
        # Test that admin can create a new course successfully
        response = self.client.post(reverse('create_course'), {
            'course_id': 101,
            'semester': 'Fall 2023',
            'name': 'Introduction to Testing',
            'description': 'A course about writing tests in Django.',
            'num_of_sections': 3,
            'modality': 'Online',
            'credits': 4
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirection after successful creation
        self.assertTrue(Course.objects.filter(name='Introduction to Testing').exists())

    def test_create_course_duplicate(self):
        # Create a course first
        Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )

        # Try to create another course with the same course_id
        response = self.client.post(reverse('create_course'), {
            'course_id': 101,
            'semester': 'Spring 2024',
            'name': 'Advanced Testing',
            'description': 'An advanced course about writing tests in Django.',
            'num_of_sections': 3,
            'modality': 'In-person',
            'credits': 4
        })
        self.assertEqual(response.status_code, 200)  # No redirection, stay on the form
        self.assertIn('A course with this ID already exists',
                      response.content.decode())  # Check for error message in response
        self.assertEqual(Course.objects.filter(course_id=101).count(), 1)  # Ensure no duplicate course was created
