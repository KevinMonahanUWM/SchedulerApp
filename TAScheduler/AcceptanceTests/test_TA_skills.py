from django.test import TestCase, Client
from TAScheduler.models import User, TA, Administrator, Course


class TASkillsUpdateSuccess(TestCase):
    user = None
    account = None
    info = None

    def setUp(self):
        self.user = Client()
        temp = User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                   last_name="Test",
                                   home_address="Random location", phone_number=9990009999)
        self.account = Administrator.objects.create(user=temp)
        ses = self.user.session
        ses["user"] = str(self.account)
        ses.save()
        self.info = {"email_address": "paul@uwm.edu", "password": "pass", "first_name": "test", "last_name": "ignore",
                     "home_address": "3400 N Maryland Ave", "phone_number": 4142292222, "role": "TA",
                     "grader_status": True}

        self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse", description="test",
                                            num_of_sections=3, modality="online")
        self.course.save()

    def test_ta_updates_skills_successfully(self):
        response = self.client.post('/ta/update_skills/', {'skills': 'Python, Teaching'})
        self.assertRedirects(response, '/some_success_page/')
        self.ta.refresh_from_db()
        self.assertEqual(self.ta.skills, 'Python, Teaching')
        self.assertContains(response, "successfully updated your skills")

    def test_ta_updates_skills_unsuccessfully(self):
        response = self.client.post('/ta/update_skills/', {'skills': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Can't assign no skills")

    def test_ta_skills_displayed_on_course_details(self):
        # Assume setup for course and TA assignment is done
        response = self.client.get('/course/details/')
        self.assertContains(response, 'Python, Teaching')  # TA's skills should be part of the response