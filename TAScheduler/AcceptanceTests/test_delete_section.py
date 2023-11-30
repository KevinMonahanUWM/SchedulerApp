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
                                modality="Remote", credits=3)
            testCourse.save()
            self.courseList.append(testCourse)
        for i in [1, 2, 3]:  # Creating 3 Sections
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList.append(testSection)
        self.lec1 = Lecture(section=self.secList[0]).save()  # Course1: Lecture
        self.lec2 = Lecture(section=self.secList[1]).save()  # Course2: Lecture
        self.lab2 = Lab(section=self.secList[2]).save()  # Course3: Lab
        self.secPostList.append(  # This is what the value of each post is
            "Lecture- Section ID:" + str(self.secList[0].section_id) + ", Course ID:" + str(self.secList[0].course_id))
        self.secPostList.append(
            "Lecture- Section ID:" + str(self.secList[1].section_id) + ", Course ID:" + str(self.secList[1].course_id))
        self.secPostList.append(
            "Lab- Section ID:" + str(self.secList[2].section_id) + ", Course ID:" + str(self.secList[2].course_id))

    # [1] Section not found in the section list
    def test_CorrectDelete(self):
        resp = self.client.post("/home/managesection/delete/", data={"sections": self.secPostList[0]})
        allSecs = Section.objects.all()
        self.assertNotIn(self.secList[0], allSecs,
                         msg="The 1st section should no longer be in the database.")

    # [2] Number of sections should have decreased if deleted properly
    def test_CorrectNumSec(self):
        oldNumSecs = Section.objects.count()
        resp = self.client.post("/home/managesection/delete/", data={"sections": self.secPostList[0]})
        newNumSecs = Section.objects.count()
        self.assertEqual(newNumSecs, oldNumSecs - 1,
                         msg="deleting a section should have decremented the number of sections in the database.")

    # [3] Success Message
    def test_confirmDelete(self):
        resp = self.client.post("/home/managesection/delete/", data={"sections": self.secPostList[0]})
        self.assertContains(resp, "Successfully Deleted Section")

    # [4] Ensure course isn't deleted, only section is
    def test_noCourseRemoved(self):
        deletedSecsCrse = self.secList[0].course
        resp = self.client.post("home/managesection/delete/", data={"section": self.secList[0]})
        allCrse = Course.objects.all()
        self.assertIn(deletedSecsCrse, allCrse,
                      msg="the course should still be in the database after removing section.")


class FailDelete(TestCase):
    client = None
    account = None
    courseList = list()

    def setUp(self):
        self.client = Client()
        self.account = Administrator.objects.create(
            user=User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                     last_name="Test",
                                     home_address="Random location", phone_number=9990009999))
        ses = self.client.session
        ses["user"] = self.account.__str__()  # should be done at login
        ses.save()
        # Creating 3 Courses
        for i in [1, 2, 3]:  # Creating 3 Courses
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credits=3)
            testCourse.save()
            self.courseList.append(testCourse)
        # Not saved in db!
        self.ghostSection = Section(section_id=2, course=self.courseList[1], location="location: ghost",
                                    meeting_time=datetime(2023, 1, 1, 1, 1, 1))

    # 1] No sections to delete
    def test_noSectionsInDBDelete(self):
        resp = self.client.get("/home/managesection/delete/")
        self.assertContains(resp, "No existing sections to delete")

    # 2] Delete non existant section shouldn't change the database
    def test_nonExistantSecDelete(self):  # possibly delete this: should never happen
        tempSecDB = Section.objects.create(section_id=1, course=self.courseList[0], location="location 1",
                                           meeting_time=datetime(2023, 1, 1, 1, 1, 1))
        Lecture.objects.create(section=tempSecDB)  # Course1: Lecture
        oldNumSecs = Section.objects.count()
        resp = self.client.post("/home/managesection/delete/", data={"sections": "Lecture- Section ID:2, Course ID:2"})
        newNumSecs = Section.objects.count()
        self.assertContains(resp, "Section does not exist in Database")
