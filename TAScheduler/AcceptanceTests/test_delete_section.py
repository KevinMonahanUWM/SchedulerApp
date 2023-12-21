# PBI #10: Delete Section
from datetime import datetime

from django.test import TestCase, Client

from TAScheduler.models import Section, Course, Lecture, Lab, Administrator, User


class SuccessDelete(TestCase):
    client = None
    account = None
    courseList = list()
    secList = list()
    secPostList = list()

    def setUp(self):
        self.client = Client()
        self.account = Administrator.objects.create(
            user=User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                     last_name="Test",
                                     home_address="Random location", phone_number=9990009999))
        ses = self.client.session
        ses["user"] = self.account.__str__()  # should be done at login
        ses.save()
        self.courseList = list()
        self.secList = list()
        for i in [1, 2, 3]:  # Creating 3 Courses
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote")
            testCourse.save()
            self.courseList.append(testCourse)
        for i in [1, 2, 3]:  # Creating 3 Sections
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList.append(testSection)
        self.lec1 = Lecture.objects.create(section=self.secList[0])  # Course1: Lecture
        self.lec2 = Lecture.objects.create(section=self.secList[1]).save()  # Course2: Lecture
        self.lab2 = Lab.objects.create(section=self.secList[2]).save()  # Course3: Lab
        self.secPostList.append(str(self.lec1))
        self.secPostList.append(str(self.lec2))
        self.secPostList.append(str(self.lab2))

    # [1] Section not found in the section list
    def test_CorrectDelete(self):
        resp = self.client.post("/home/managesection/", data={"section": self.secPostList[0], 'delete': 'Delete'})
        allSecs = Section.objects.all()
        self.assertNotIn(self.secList[0], allSecs,
                         msg="The 1st section should no longer be in the database.")

    # [2] Number of sections should have decreased if deleted properly
    def test_CorrectNumSec(self):
        oldNumSecs = Section.objects.count()
        resp = self.client.post("/home/managesection/", data={"section": self.secPostList[0], 'delete': 'Delete'})
        newNumSecs = Section.objects.count()
        self.assertEqual(newNumSecs, oldNumSecs - 1,
                         msg="deleting a section should have decremented the number of sections in the database.")

    # [3] Success Message
    def test_confirmDelete(self):
        resp = self.client.post("/home/managesection/", data={"section": self.secPostList[0], 'delete': 'Delete'})
        self.assertContains(resp, "Successfully Deleted Section")

    # [4] Ensure course isn't deleted, only section is
    def test_noCourseRemoved(self):
        deletedSecsCrse = self.secList[0].course
        resp = self.client.post("home/managesection/", data={"section": self.secPostList[0], 'delete': 'Delete'})
        allCrse = Course.objects.all()
        self.assertIn(deletedSecsCrse, allCrse,
                      msg="the course should still be in the database after removing section.")
