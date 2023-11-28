# PBI #9: Creating Section
from datetime import datetime

from django.test import TestCase, Client

from TAScheduler.models import Section, Course, Lecture, Lab, Administrator, User


# Ideas for other tests...
# 3] check in Database (all fields matching) x2 for [lab+lecture]
# 4] display .context[] confirmation response
# 5] check course ID against database (Requirements: Unique + must exist)
# 6] check section ID against database (Requirements: Unique -doesn't need to exist bc we're creating here-)
# - Notes: 1] We're missing "AC4"] Max Course Sections: Check that course1 can't accept any more sections (full course)
# 2] database missing "hours" for section 3] IDK how to deal with dropdowns

# AC1] - Success (Inputs/Course Exists, Unique ID)
class Create(TestCase):  # 6/6 Pass
    client = None
    account = None
    info = None
    courseList = None
    secList = None

    def setUp(self):
        self.client = Client()
        self.account = Administrator.objects.create(
            user=User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                     last_name="Test",
                                     home_address="Random location", phone_number=9990009999))
        ses = self.client.session
        ses["user"] = "testadmin@uwm.edu"  # should be done at login
        ses.save()
        self.courseList = list()  # holding list of test courses so easier to call later
        self.secList = list()
        for i in [1, 2, 3]:  # Creating 3 Courses: hardcoded "numSec","modality","credits"
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credits=3)
            testCourse.save()
            self.courseList.append(testCourse)
        for i in [1, 2, 3]:  # Creating 3 Sections: hardcoded "meetingTime"
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList.append(testSection)
        self.lec1 = Lecture(section=self.secList[0]).save()  # Course1: Lecture
        self.lec2 = Lecture(section=self.secList[1]).save()  # Course2: Lecture
        self.lab2 = Lab(section=self.secList[2]).save()  # Course3: Lab
        # For user's input ...
        self.lecInfo = {"course_id": self.courseList[2].course_id, "section_id": 4, "section_type": "Lecture",
                        "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "location": "location" + str(4)
                        }
        self.labInfo = {"course_id": self.courseList[2].course_id, "section_id": 4, "section_type": "Lab",
                        "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "location": "location" + str(4)
                        }

    # [1] Creating Unique Lecture:
    def test_SuccessfulLecCreation(self):
        origDBSecCount = Section.objects.all().count()
        resp = self.client.post("/home/managesection/create", data=self.lecInfo)
        newDBSecCount = Section.objects.all().count()
        newSecDB = Section.objects.get(section_id=4)
        newLecDBQS = Lecture.objects.filter(section=newSecDB)
        self.assertTrue(newLecDBQS.count() == 1,
                        msg="should have found the newly added lecture in db")
        self.assertTrue(newDBSecCount == (origDBSecCount + 1),
                        msg="there needs to be an extra section when creating a section")

    # [2] Creating Unique Lab
    def test_SuccessfulLabCreation(self):
        resp = self.client.post("/home/managesection/create", data=self.labInfo)
        newSecDB = Section.objects.get(section_id=4)
        newLabDBQS = Lab.objects.filter(section=newSecDB)
        self.assertTrue(newLabDBQS.count() is 1,
                        msg="should have found the newly added lab in db")

    # [3] DB Change: # of secs incremented ("adding" lec)
    def test_additionalLec(self):
        origDBSecCount = Section.objects.all().count()
        resp = self.client.post("/home/managesection/create", data=self.lecInfo)
        newDBSecCount = Section.objects.all().count()
        self.assertTrue(newDBSecCount == (origDBSecCount + 1),
                        msg="there needs to be an extra section when creating a section")

    # [4] DB Change: # of secs incremented ("adding" lab)
    def test_additionalLab(self):
        origDBSecCount = Section.objects.all().count()
        resp = self.client.post("/home/managesection/create", data=self.labInfo)
        newDBSecCount = Section.objects.all().count()
        self.assertTrue(newDBSecCount == (origDBSecCount + 1),
                        msg="there needs to be an extra section when creating a section")

    # [5] Confirmation message for lecture
    def test_ConfirmLec(self):
        resp = self.client.post("/home/managesection/create", data=self.lecInfo)
        self.assertContains(resp, "Successfully Created Section",
                            status_code=200)  # couldn't find "message" in ".context" so doing this way

    # [6] Confirmation message for lab
    def test_ConfirmLab(self):
        resp = self.client.post("/home/managesection/create", data=self.labInfo)
        self.assertContains(resp, "Successfully Created Section", status_code=200)


# AC2] - Duplicate Section (not unique in the database)
class NoCreateDupeSec(TestCase):  # 4/4 Pass
    client = None
    account = None
    info = None
    courseList = None
    secList = None

    def setUp(self):
        self.client = Client()
        self.account = Administrator.objects.create(
            user=User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                     last_name="Test",
                                     home_address="Random location", phone_number=9990009999))
        ses = self.client.session
        ses["user"] = "testadmin@uwm.edu"  # should be done at login
        ses.save()
        self.courseList = list()
        self.secList = list()
        for i in [1, 2, 3]:  # Creating 3 Courses:
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credits=3)
            testCourse.save()
            self.courseList.append(testCourse)
        for i in [1, 2, 3]:  # Creating 3 Sections:
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList.append(testSection)
        # For user's input: Duped with "section 1" for a lecture & lab
        self.dupedLecInfo = {"course_id": self.courseList[2].course_id, "section_id": 1, "section_type": "Lecture",
                             "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "location": "location" + str(4)
                             }
        self.dupedLabInfo = {"course_id": self.courseList[2].course_id, "section_id": 1, "section_type": "Lab",
                             "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "location": "location" + str(4)
                             }

    # [1] Creating NON-unique Lecture: id=1
    def test_dupeSectionToLecture(self):
        resp = self.client.post("/home/managesection/create", data=self.dupedLecInfo)
        self.assertContains(resp, "Section with this ID already exists")

    # [2] Creating NON-unique Lab: id=1
    def test_dupeSectionToLab(self):
        resp = self.client.post("/home/managesection/create", data=self.dupedLabInfo)
        self.assertContains(resp, "Section with this ID already exists")

    # [3] No DB Change: # of secs same ("adding" lec)
    def test_noAdditionalLec(self):
        origDBSecCount = Section.objects.all().count()
        resp = self.client.post("/home/managesection/create", data=self.dupedLecInfo)
        newDBSecCount = Section.objects.all().count()
        self.assertTrue(newDBSecCount == origDBSecCount,
                        msg="should not have changed the amount of sections when creating dupe sec")

    # [4] No DB Change: # of secs same ("adding" lab)
    def test_noAdditionalLab(self):
        origDBSecCount = Section.objects.all().count()
        resp = self.client.post("/home/managesection/create", data=self.dupedLabInfo)
        newDBSecCount = Section.objects.all().count()
        self.assertTrue(newDBSecCount == origDBSecCount,
                        msg="should not have changed the amount of sections when creating dupe sec")


# AC3] - Nonexistant Course
class NonexistantCourse(TestCase): # 4/4 pass
    client = None
    account = None
    info = None
    courseList = None
    secList = None

    def setUp(self):
        self.client = Client()
        self.account = Administrator.objects.create(
            user=User.objects.create(email_address="testadmin@uwm.edu", password="pass", first_name="Test",
                                     last_name="Test",
                                     home_address="Random location", phone_number=9990009999))
        ses = self.client.session
        ses["user"] = "testadmin@uwm.edu"  # should be done at login
        ses.save()
        self.courseList = list()
        self.secList = list()
        for i in [1, 2, 3]:  # Creating 3 Courses:
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credits=3)
            testCourse.save()
            self.courseList.append(testCourse)
        for i in [1, 2, 3]:  # Creating 3 Sections:
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList.append(testSection)
        badCourse = Course(course_id=4)  # not saved to database!
        self.badCrsIDLecInfo = {"section_id": 4, "course": badCourse.course_id, "location": "location" + str(4),
                                "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "secType": "Lecture"}
        self.badCrsIDLabInfo = {"section_id": 4, "course": badCourse.course_id, "location": "location" + str(4),
                                "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "secType": "Lab"}

    # [1] Creating missing input lec
    def test_missingInput(self):
        invalidSecInfo = {"course_id": "",
                          "section_id": "",
                          "section_type": "",
                          "meeting_time": "",
                          "location": ""}
        resp = self.client.post("/home/managesection/create", data=invalidSecInfo)
        self.assertContains(resp, "No missing section fields allowed")

    # [2] Error Message lec
    def test_errorMsgNoExistCourse(self):
        resp = self.client.post("/home/managesection/create", data=self.badCrsIDLecInfo)
        self.assertContains(resp, "Course ID is not existing course cant create section")

    # [3] No DB Change: # of secs same ("adding" lec)
    def test_noAdditionalLec(self):
        oldNumSecs = Section.objects.count()
        resp = self.client.post("/home/managesection/create", data=self.badCrsIDLecInfo)
        newNumSecs = Section.objects.count()
        self.assertEqual(oldNumSecs, newNumSecs,
                          msg="should not have changed the amount of sections when creating non-existant course")

    # [4] Error Message lec
    def test_errorMsgNoExistCourse(self):
        resp = self.client.post("/home/managesection/create", data=self.badCrsIDLabInfo)
        self.assertContains(resp, "Course ID is not existing course cant create section")

    # [5] No DB Change: # of secs same ("adding" lab)
    def test_noAdditionalLab(self):
        origDBSecCount = Section.objects.all().count()
        resp = self.client.post("/home/managesection/create", data=self.badCrsIDLabInfo)
        newDBSecCount = Section.objects.all().count()
        self.assertTrue(newDBSecCount == origDBSecCount,
                        msg="should not have changed the amount of sections when creating non-existant course")

