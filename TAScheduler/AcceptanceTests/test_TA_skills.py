from django.test import TestCase, Client

from TAScheduler.models import User, Instructor, Course, TA, Section, Lecture, Lab, Administrator
from TAScheduler.view_methods.ta_methods import TAObj
from TAScheduler.view_methods.instructor_methods import InstructorObj


class SuccessfulCreation(TestCase):
    ta = None
    instructor = None
    section = None
    user = None

    def setUp(self):
        self.client = Client()

        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()
        self.ta = TA.objects.create(
            user=temp,
            skills="",
            grader_status=True
        )
        self.course = Course.objects.create(
            course_id=101,
            semester="Fall",
            name="Intro to Testing",
            description="A course about writing tests",
            num_of_sections=1,
            modality="Online"
        )

    def test_ta_updates_skills_successfully(self):
        # TA updates their skills
        response = self.client.post('/home/manageaccount/edit/', {
            'skills': 'Python, Teaching'
        })

        # Verify that the TA's skills were updated
        self.ta.refresh_from_db()
        self.assertEqual(self.ta.skills, 'Python, Teaching')
        # Assuming that the success message is part of the response context
        self.assertContains(response, "successfully updated your skills")

        # Verify that the TA's skills are displayed on the course details page
        response = self.client.get(f'/home/managecourse/{self.course.course_id}/details/')
        self.assertContains(response, self.ta.skills)

    def test_ta_updates_skills_unsuccessfully(self):
        # TA attempts to list no skills
        response = self.client.post('/home/manageaccount/edit/', {

            'skills': ''
        })

        # Verify that an error message is displayed
        self.assertContains(response, "Can't assign no skills")
