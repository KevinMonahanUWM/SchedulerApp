# PBI #11: Edit Section
from datetime import datetime

from django.test import TestCase, Client

from TAScheduler.models import Section, Course, Lecture, Lab


# AC1] - Successful Edit (>0 sections, valid changes, no missing)
class SuccessEdit(TestCase):
    def setUp(self):
        self.client = Client()
        self.courseList = list()  # holding list of test courses so easier to call later
        self.secList = list()
        for i in [1, 2, 3]:  # Creating 3 Courses: hardcoded "numSec","modality","credits"
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credts=3, )
            testCourse.save()
            self.courseList = self.courseList.append(testCourse)
        for i in [1, 2, 3]:  # Creating 3 Sections: hardcoded "meetingTime"
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList = self.secList.append(testSection)

    # 1] Database reflects our input
    def test_DatabaseEditChange(self):
        secChanges = {"location": "Naboo"}  # probs need to send "all" fields
        resp = self.client.post("home/managesection/edit", data={"section": self.secList[0], "edit": secChanges})
        dbEditedSect = Section.objects.filter(section_id=self.secList[0].section_id)
        self.assertEquals(dbEditedSect["location"], "Naboo")

    # 2] Confirmation message
    def test_ConfirmationMessage(self):
        secChanges = {"location": "Naboo"}  # ^
        resp = self.client.post("home/managesection/edit", data={"section": self.secList[0], "edit": secChanges})
        self.assertEquals(resp.context["message"], "SUCCESSFULLY CHANGED INFORMATION")


# AC2] - Unsuccessful (invalid changes)
class UnSuccessEdit(TestCase):
    def setUp(self):
        self.client = Client()
        self.courseList = list()  # holding list of test courses so easier to call later
        self.secList = list()
        for i in [1, 2, 3]:  # Creating 3 Courses: hardcoded "numSec","modality","credits"
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credts=3, )
            testCourse.save()
            self.courseList = self.courseList.append(testCourse)
        for i in [1, 2, 3]:  # Creating 3 Sections: hardcoded "meetingTime"
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList = self.secList.append(testSection)

    def test_MissingFields(self):
        secChanges = Section(section_id="", course="", location="", meeting_time="")
        resp = self.client.post("home/managesection/edit", data={"section": self.secList[0], "edit": secChanges})
        self.assertEquals(resp.context["message"], "MISSING SECTION FIELDS")

    # add these if we're going to allow editing of lectures/labs.
    # def test_NonExistantUserAsgmt(self):
    # def test_NonExistantCourse(self):#


# AC3] - Discard
class DiscardEdit(TestCase):
    def setUp(self):
        self.client = Client()
        self.courseList = list()  # holding list of test courses so easier to call later
        self.secList = list()
        for i in [1, 2, 3]:  # Creating 3 Courses: hardcoded "numSec","modality","credits"
            testCourse = Course(course_id=i, semester="semester" + str(i), name="name" + str(i), num_of_sections=2,
                                modality="Remote", credts=3, )
            testCourse.save()
            self.courseList = self.courseList.append(testCourse)
        for i in [1, 2, 3]:  # Creating 3 Sections: hardcoded "meetingTime"
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList = self.secList.append(testSection)

    # 1] Get fields from database, ensure they're what originally.
    def test_DataRestored(self):
        secChanges = {"location": "Naboo"}  # probs need to send "all" fields
        resp = self.client.post("home/managesection/edit",
                                {"section": self.secList[0], "edit": secChanges, "discard_changes": 'Discard Changes'})
        self.assertEquals(Section.objects.get(section_id= self.secList[0].section_id).location, "location1")

    # 2] Replace this with the specific URL when done
    def test_Redirected(self):
        resp = self.client.post("home/managesection/edit", {'discard_changes': 'Discard Changes'})
        self.assertEquals(resp.status_code, 302, msg="discarding changes should have redirected")


    # 3] probably replace the message.
    def test_ConfirmationMsg(self):
        pass
        # going to fill this out later.

