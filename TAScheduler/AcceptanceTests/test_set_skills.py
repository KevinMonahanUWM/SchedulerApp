from django.test import TestCase, Client

from TAScheduler.models import User, TA, Course, TAToCourse, Administrator


class SuccessSetSkills(TestCase):
    user = None
    TA = None
    course = None
    taList = list()

    def setUp(self):
        self.user = Client()
        for i in [1, 2]:
            self.taList.extend(TA.objects.create(  # grader status = True, no skills, max assignments = 2
                user=User.objects.create(
                    email_address="admin@uwm.edu" + str(i),
                    password="pass" + str(i),
                    first_name="test" + str(i),
                    last_name="test" + str(i),
                    home_address="home" + str(i),
                    phone_number=1234567890
                ),
                grader_status=True,
                skills="No skills listed",
                max_assignments=2
            ))
            ses = self.client.session
            ses["user"] = self.taList[0].__str__()  # not sure if this should be "Administrator"
            ses.save()

            self.course = Course.objects.create(course_id=100, semester="fall 2023", name="testCourse",
                                                description="test",
                                                num_of_sections=3, modality="online")
            TAToCourse.objects.create(ta=self.taList[0], course=self.course)  # assigning 1st TA to course

    def successTASetSkills(self):
        resp = self.user.post("/home/managecourse/edit/", {
            "skills": "Not as good as Kevin"})  # not sure what the variable is called, it's not in this branch's HTML
        self.assertEqual(self.taList[0], "Not as good as Kevin", msg="Should have changed skills in setSkills")


