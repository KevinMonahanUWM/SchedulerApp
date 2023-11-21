# PBI #9: Creating Section
from datetime import datetime

from django.test import TestCase, Client

from TAScheduler.models import Section, Course, Lecture, Lab


# Ideas for other tests...
# 3] check in Database (all fields matching) x2 for [lab+lecture]
# 4] display .context[] confirmation response
# 5] check course ID against database (Requirements: Unique + must exist)
# 6] check section ID against database (Requirements: Unique -doesn't need to exist bc we're creating here-)
# MISSING "AC4"] Max Course Sections: Check that course1 can't accept any more sections (full course)
# !OUR DATABASE IS MISSING "hours" FOR SECTION!

# AC1] - Success (Inputs/Course Exists, Unique ID)
class Create(TestCase):
    def setUp(self):
        self.client = Client()
        self.courseList = list()  # holding list of test courses so easier to call later
        self.secList = list()
        # Creating 3 Courses: hardcoded "numSec","modality","credits"
        for i in [1, 2, 3]:
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credts=3, )
            testCourse.save()
            self.courseList = self.courseList.append(testCourse)
        ### !!!DON'T KNOW IF THIS PART IS NEEDED YET!!!
        # Creating 3 Sections: hardcoded "meetingTime"
        for i in [1, 2, 3]:
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList = self.secList.append(testSection)
        # Assigning course1: lecture + lab ... course2: lecture ... course3: <- No Users assigned.
        self.lec1 = Lecture(section=self.secList[0], ).save
        self.lec2 = Lecture(section=self.secList[1]).save
        self.lab1 = Lab(section=self.secList[2]).save
        ### ^^^
        # For user's input ...
        self.lecInfo = {"section_id": 4, "course": self.courseList[2], "location": "location" + 4,
                        "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "secType": "Lecture"}
        self.labInfo = {"section_id": 4, "course": self.courseList[2], "location": "location" + 4,
                        "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "secType": "Lab"}

    # 1] Creating Unique Lecture w/ Existing course & all inputs
    # IDK HOW TO SEND IN "LECTURE" AS A DROPDOWN IN POST
    def test_SuccessfulLecCreation(self):
        resp = self.client.post("home/managesection/edit", data=self.lecInfo)
        self.assertTrue(Lecture.objects.filter(section_id=4).count() is 1,
                        msg="should have found the newly added lecture in db")

    # 2] Creating Unique Lab w/ Existing course & all inputs
    def test_SuccessfulLabCreation(self):
        resp = self.client.post("home/managesection/edit", data=self.labInfo)
        self.assertTrue(Lab.objects.filter(section_id=4).count() is 1,
                        msg="should have found the newly added lab in db")

    # 3] Confirmation message for lecture
    def test_ConfirmLec(self):
        resp = self.client.post("home/managesection/edit", data=self.lecInfo)
        self.assertEquals(resp.context["message"], "successfully created Lecture",
                          "Should've returned confirmation message for creating lecture")

    # 4] Confirmation message for lab
    def test_ConfirmLab(self):
        resp = self.client.post("home/managesection/edit", data=self.labInfo)
        self.assertEquals(resp.context["message"], "successfully created Lab",
                          "Should've returned confirmation message for creating lab")


# AC2] - Duplicate Section (not unique in the database)
class NoCreateDupeSec(TestCase):
    def setUp(self):
        self.client = Client()
        self.courseList = list()  # holding list of test courses so easier to call later
        self.secList = list()
        # Creating 3 Courses: hardcoded "numSec","modality","credits"
        for i in [1, 2, 3]:
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credts=3, )
            testCourse.save()
            self.courseList = self.courseList.append(testCourse)
        ### !!!DON'T KNOW IF THIS PART IS NEEDED YET!!!
        # Creating 3 Sections: hardcoded "meetingTime"
        for i in [1, 2, 3]:
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList = self.secList.append(testSection)
        # Assigning course1: lecture + lab ... course2: lecture ... course3: <- No Users assigned.
        self.lec1 = Lecture(section=self.secList[0], ).save
        self.lec2 = Lecture(section=self.secList[1]).save
        self.lab1 = Lab(section=self.secList[2]).save
        ### ^^^
        # For user's input ...
        self.dupedLecIDInfo = {"section_id": 1, "course": self.courseList[2], "location": "location" + 4,
                               "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "secType": "Lecture"}
        self.dupedLabIDInfo = {"section_id": 1, "course": self.courseList[2], "location": "location" + 4,
                               "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "secType": "Lab"}

    # 1] Error Message: Dupe lecture
    def test_UnsuccessfulLecCreationDupe(self):
        resp = self.client.post("home/managesection/edit", data=self.dupedLecIDInfo)
        self.assertEquals(resp.context["message"], "BAD ID: TRIED TO CREATE DUPLICATE SECTION",
                          msg="can't instantiate lecture already existing")

    # 2] Error Message: Dupe lab
    def test_UnsuccessfulLabCreationDupe(self):
        resp = self.client.post("home/managesection/edit", data=self.dupedLabIDInfo)
        self.assertEquals(resp.context["message"], "BAD ID: TRIED TO CREATE DUPLICATE SECTION",
                          msg="can't instantiate lab already existing")

    # 3] No DB Change: # of secs same ("adding" lec)
    def test_UnsuccessfulLecCreationNoDBChange(self):
        oldNumSecs = Section.objects.count()
        resp = self.client.post("home/managesection/edit", data=self.dupedLecIDInfo)
        newNumSecs = Section.objects.count()
        self.assertEquals(oldNumSecs, newNumSecs, msg="adding duped lecture shouldn't have incremented number of secs")

    # 4] No DB Change: # of secs same ("adding" lab)
    def test_UnsuccessfulLabCreationNoDBChange(self):
        oldNumSecs = Section.objects.count()
        resp = self.client.post("home/managesection/edit", data=self.dupedLabIDInfo)
        newNumSecs = Section.objects.count()
        self.assertEquals(oldNumSecs, newNumSecs, msg="adding duped lab shouldn't have incremented number of secs")


# AC3] - Nonexistant Course
class NonexistantCourse(TestCase):
    def setUp(self):
        self.client = Client()
        self.courseList = list()  # holding list of test courses so easier to call later
        self.secList = list()
        # Creating 3 Courses: hardcoded "numSec","modality","credits"
        for i in [1, 2, 3]:
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credts=3, )
            testCourse.save()
            self.courseList = self.courseList.append(testCourse)
        ### !!!DON'T KNOW IF THIS PART IS NEEDED YET!!!
        # Creating 3 Sections: hardcoded "meetingTime"
        for i in [1, 2, 3]:
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList = self.secList.append(testSection)
        # Assigning course1: lecture + lab ... course2: lecture ... course3: <- No Users assigned.
        self.lec1 = Lecture(section=self.secList[0], ).save
        self.lec2 = Lecture(section=self.secList[1]).save
        self.lab1 = Lab(section=self.secList[2]).save
        ### ^^^
        badCourse = Course(course_id=4)  # not saved to database!
        self.badCrsIDLecInfo = {"section_id": 4, "course": badCourse, "location": "location" + 4,
                                "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "secType": "Lecture"}
        self.badCrsIDLabInfo = {"section_id": 4, "course": badCourse, "location": "location" + 4,
                                "meeting_time": datetime(2023, 1, 1, 1, 1, 1), "secType": "Lab"}

    # 1] Error Message
    def test_ErrorMsgNoExistCourse(self):
        resp = self.client.post("home/managesection/edit", data=self.badCrsIDLecInfo)
        self.assertEquals(resp.context["message"], "BAD HOST COURSE ID: COURSE DOES NOT EXIST",
                          msg="can't instantiate lecture already existing")

    # 2] No DB Change: # of secs same ("adding" lec)
    def test_NoDBChangeNoExistCourse(self):
        oldNumSecs = Section.objects.count()
        resp = self.client.post("home/managesection/edit", data=self.badCrsIDLecInfo)
        newNumSecs = Section.objects.count()
        self.assertEquals(oldNumSecs, newNumSecs,
                          msg="adding bad host couse ID'ed lecture shouldn't have incremented number of secs")

# 3] repeat 1] for lab#
# 4] repeat 2] for lab
