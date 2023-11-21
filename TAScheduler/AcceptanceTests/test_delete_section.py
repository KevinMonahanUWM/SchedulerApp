# PBI #10: Delete Section
from datetime import datetime

from django.test import TestCase, Client

from TAScheduler.models import Section, Course, Lecture, Lab


class SuccessDelete(TestCase):
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
        # Creating 3 Sections: hardcoded "meetingTime"
        for i in [1, 2, 3]:
            testSection = Section(section_id=i, course=self.courseList[i - 1], location="location" + str(i),
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))
            testSection.save()
            self.secList = self.secList.append(testSection)
##
    # 1] Section not found in the section list
    def test_correctDelete(self):
        resp = self.client.post("home/managesection/delete", data={"section": self.secList[0]})
        self.assertNotIn(self.secList[0], Section.objects.all,
                         msg="The 1st section should no longer be in the database.")

    # 2] Number of sections should have decreased if deleted properly
    def test_correctNumSec(self):
        oldNumSecs = Section.objects.count()
        resp = self.client.post("home/managesection/delete", data={"section": self.secList[0]})
        newNumSecs = Section.objects.count()
        self.assertEquals(newNumSecs, oldNumSecs - 1,
                          msg="deleting a section should have decremented the number of sections in the database.")

    # 3] Success Message
    def test_confirmDelete(self):
        resp = self.client.post("home/managesection/delete", data={"section": self.secList[0]})
        self.assertNotIn(resp.context["message"], "successfully deleted section",
                         msg="The 1st section should no longer be in the database.")


class FailDelete(TestCase):
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
        #Not saved in db!
        self.ghostSection = Section(section_id=1, course=self.courseList[0], location="location" + 1,
                                  meeting_time=datetime(2023, 1, 1, 1, 1, 1))

    # 1] No sections to delete
    def test_noSectionsInDBDelete(self):
        resp = self.client.post("home/managesection/delete",follow=True)
        self.assertNotIn(resp.context["message"], "No Existing Section to Delete.",
                         msg="Entering delete section w/o any sections should display error")

    # 2] Delete non existant section, with "full" db, shouldn't change the database
    def test_nonExistantSecDelete(self):
        oldNumSecs = Section.objects.count()
        resp = self.client.post("home/managesection/delete",data = {"section": self.ghostSection})
        newNumSecs = Section.objects.count()
        self.assertEquals(newNumSecs, oldNumSecs ,
                          msg="deleting a non-existant section shouldn't change database")



