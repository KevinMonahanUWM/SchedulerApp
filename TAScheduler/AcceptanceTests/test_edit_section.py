# PBI #11: Edit Section
from datetime import datetime

from django.test import TestCase, Client

from TAScheduler.models import Section, Course, Lecture, Lab, Administrator, User


# AC1] - Successful Edit (>0 sections, valid changes, no missing)
class SuccessEdit(TestCase):
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
        self.lec2 = Lecture.objects.create(section=self.secList[1])  # Course2: Lecture
        self.lab2 = Lab.objects.create(section=self.secList[2])  # Course3: Lab
        self.secPostList.append(str(self.lec1))
        self.secPostList.append(str(self.lec2))
        self.secPostList.append(str(self.lab2))
        ses["current_edit"] = self.secPostList[0]
        ses.save()

    # [1] Database reflects our input
    def test_DatabaseEditChange(self):
        print(self.client.session["current_edit"])
        resp = self.client.post("/home/managesection/edit/",
                                {"section_id": str(self.secList[0].section_id),
                                      "location": "Naboo",
                                      "meeting_time": self.secList[0].meeting_time})
        dbEditedSect = Section.objects.filter(section_id=self.secList[0].section_id)[0]
        self.assertEqual(dbEditedSect.location, "Naboo")


# AC2] - Unsuccessful (invalid changes)
class UnSuccessEdit(TestCase):
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
        self.lec2 = Lecture.objects.create(section=self.secList[1])  # Course2: Lecture
        self.lab2 = Lab.objects.create(section=self.secList[2])  # Course3: Lab
        self.secPostList.append(str(self.lec1))
        self.secPostList.append(str(self.lec2))
        self.secPostList.append(str(self.lab2))
        ses["current_edit"] = self.secPostList[0]
        ses.save()

    # [1] Ensure "no change" doesn't change the DB.
    def test_DatabaseEditChange(self):

        resp = self.client.post("/home/managesection/edit/",
                                data={"section_id": str(self.secList[0].section_id),
                                      "meeting_time": self.secList[0].meeting_time})
        dbEditedSect = Section.objects.filter(section_id=self.secList[0].section_id)[0]
        self.assertEqual(dbEditedSect.location, "location1")
