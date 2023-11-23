import unittest
import datetime

from django.test import TestCase

from TAScheduler.models import Course, User, TA, Section, Lab, Administrator, Instructor, InstructorToCourse
from TAScheduler.views_methods import CourseObj, AdminObj, TAObj, LabObj, SectionObj, InstructorObj, LectureObj


# PBI Assignments ...
# Alec = #1,#2 (Total = 6)
# Kevin = #3,#4,#5 (Total = 4)
# Randall = #6,#7,#8 (Total = 12)
# Kiran = #9,#10,#11 (Total = 15)
# Joe = #12,#13 (Total = 8)
# SEE METHOD DESCRIPTIONS FOR GUIDE ON HOW TO WRITE.
# Feel free to make suggestions on discord (add/remove/edit methods)!.
### Rememeber: These methods were made before any coding (I was guessing) so it's likely they should be changed.
class TestUserLogin(TestCase):  # Alec
    pass


class TestUserGetID(TestCase):  # Alec
    pass


class TestUserGetPassword(TestCase):  # Alec
    pass


class TestUserGetName(TestCase):  # Alec
    pass


class TestUserGetRole(TestCase):  # Alec
    pass


class TestAdminInit(TestCase):
    pass
  
class TestAdminCreateCourse(TestCase):  # Alec
    pass


class TestAdminCreateUser(TestCase):  # Alec
    pass


class TestAdminCreateSection(TestCase):  # Alec
    pass


class TestAdminRemoveCourse(TestCase):  # Kevin
    pass


class TestAdminRemoveAccount(TestCase):  # Kevin
    pass


class TestAdminRemoveSection(TestCase):  # Kevin
    pass


class TestAdminEditCourse(TestCase):  # Kevin
    pass


class TestAdminEditSection(TestCase):  # Kevin
    pass


class TestAdminEditAccount(TestCase):  # Kevin
    pass


class TestAdminCourseInstrAsgmt(TestCase):  # Kevin
    pass


class TestAdminCourseTAAsgmt(TestCase):  # Kevin
    pass

class TestTAInit(TestCase):
    pass

class TestTAHasMaxAsgmts(TestCase):  # Kiran
    pass


class TestTAAssignTACourse(TestCase):  # Kiran
    pass


class TestTAGetTACrseAsgmts(TestCase):  # Kiran
    pass


class TestAssignTALab(TestCase):
    pass


class TestTAGetTALabAsgmts(TestCase):  # Kiran
    pass


class TestAssignTALec(TestCase):
    pass


class TestTAGetTALecAsgmts(TestCase):  # Kiran
    pass


class TestTAGetGraderStatus(TestCase):  # Kiran
    pass

class TestInstrutorInit(TestCase):
    pass


class TestInstructorHasMaxAsgmts(TestCase):  # Kiran
    pass


class TestInstructorAssignInstrCourse(TestCase):  # Kiran
    pass


class TestInstructorGetInstrCrseAsgmts(TestCase):  # Kiran
    pass


class TestInstructorAssignInstrLec(TestCase):  # Kiran
    pass


class TestInstructorGetInstrLecAsgmts(TestCase):  # Kiran
    pass


class TestInstructorLecTAAsmgt(TestCase):
    pass


class TestInstructorLabTAAsmgt(TestCase):
    pass
  
  
class TestCourseInit(TestCase):
    pass


class TestCourseAddInstructor(TestCase):  # Randall
    pass


class TestCourseAddTA(TestCase):  # Randall
    pass


class TestCourseRemoveAssignment(TestCase):  # Randall
    pass


class TestCourseRemoveCourse(TestCase):  # Randall
    pass


class TestCourseEditCourseInfo(TestCase):  # Randall
    pass


class TestCourseGetAsgmtsForCrse(TestCase):  # Randall
    pass


class TestCourseGetSectionsForCrse(TestCase):  # Randall
    pass


class TestCourseGetCrseInfo(TestCase):  # Randall
    pass



class TestSectionGetID(unittest.TestCase):  # Joe
    section = None
    course = None

    def setUp(self):
        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        self.course.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()
        self.section = SectionObj(hold_section)

    def test_get_id(self):
        self.assertEquals(self.section.getID(), 1011, "getID() did not retrieve correct section_id")

    # Maybe test for section_id = None, but I don't think section can be made without


class TestSectionGetParentCourse(unittest.TestCase):  # Joe
    section = None
    course = None

    def setUp(self):
        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        self.course.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()
        self.section = SectionObj(hold_section)

    def test_get_parent_course(self):
        self.assertEquals(self.section.getParentCourse(), self.course,
                          "getParentCourse() did not retrieve correct course")


class TestLabInit(unittest.TestCase):
    section = None
    course = None
    lab = None

    def setUp(self):
        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        self.course.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()

        self.section = SectionObj(hold_section)
        self.lab = LabObj(self.section)

    def test_lab_make(self):
        self.assertIsNotNone(self.lab.__init__(), "__init__ failed in making Lab")


class TestLabGetLabTAAsgmt(unittest.TestCase):  # Joe
    lab = None
    ta = None

    def setUp(self):
        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmpcourse.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()
        hold_section_lab = SectionObj(hold_section)
        self.lab = LabObj(hold_section_lab)

    def test_get_ta(self):
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        self.assertEquals(self.ta, self.lab.getLabTAAsgmt(), "getLabTAAsgmt() does not retrieve ta")

    def test_no_ta(self):
        self.assertIsNone(self.lab.getLabTAAsgmt(), "getLabTAAsgmt() finds something with no TA")


class TestLabAddTA(unittest.TestCase):  # Joe
    lab = None
    ta = None

    def setUp(self):
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmpcourse.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()
        hold_section_lab = SectionObj(hold_section)
        self.lab = LabObj(hold_section_lab)

    def test_add_ta(self):
        temp2 = User(email_address="test2@test.com", password="password2", first_name="first2", last_name="last2",
                     home_address="Your mom's house", phone_number=1234567890)
        temp2.save()

        tempta = TA.objects.create(user=temp2)
        tempta.save()
        self.lab.addTA(tempta)
        self.assertIn(tempta, self.lab, "addTA() does not add TA")  # Can't write tests without container

    def test_full(self):
        temp2 = User(email_address="test2@test.com", password="password2", first_name="first2", last_name="last2",
                     home_address="Your mom's house", phone_number=1234567890)
        temp2.save()

        tempta = TA.objects.create(user=temp2)
        tempta.save()
        self.lab.addTA(tempta)
        with self.assertRaises(RuntimeError, msg="Tried to add TA to full Lab"):
            self.lab.addTA(self.ta)


class TestLabRemoveTA(unittest.TestCase):  # Joe
    lab = None
    ta = None

    def setUp(self):
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmpcourse.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()
        hold_section_lab = SectionObj(hold_section)
        self.lab = LabObj(hold_section_lab)

    def test_remove(self):
        self.lab.removeTA()
        self.assertNotIn(self.ta, self.lab, "removeTA() does not remove TA")  # Can't write tests without container


class TestLectureInit(unittest.TestCase):
    section = None
    course = None
    lecture = None

    def setUp(self):
        self.course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        self.course.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()

        tempsection = SectionObj(hold_section)
        self.lecture = LectureObj(tempsection)

    def test_lecture_make(self):
        self.assertIsNotNone(self.lecture.__init__(), "__init__ failed in making Lecture")


class TestLectureGetLecInstrAsgmt(unittest.TestCase):  # Joe
    instructor = None
    lecture = None

    def setUp(self):
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()


        self.instructor = Instructor.objects.create(user=temp)
        self.instructor.save()

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmpcourse.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()

        tempsection = SectionObj(hold_section)
        self.lecture = LectureObj(tempsection)

    def test_get_instructor(self):
        self.assertEquals(self.instructor, self.lecture.getLecInstrAsmgt(), "getLecInstrAsmgt() does not return correct")

    def test_get_but_none(self):
        with self.assertRaises(RuntimeError, msg="Tried to retrieve from none"):
            self.lecture.getLecInstrAsmgt()



class TestLectureAddInstructor(unittest.TestCase):  # Joe
    instructor = None
    lecture = None

    def setUp(self):
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp)
        self.instructor.save()

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmpcourse.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()

        tempsection = SectionObj(hold_section)
        self.lecture = LectureObj(tempsection)

    def test_add_but_full(self):
        self.lecture.addInstr(self.instructor)
    def test_add(self):
        self.lecture.addInstr(self.instructor)
        self.assertIsNotNone(self.lecture.getLecInstrAsmgt(), "getLecInstrAsmgt() Did not add instructor")

class TestLectureRemoveInstructor(unittest.TestCase):  # Joe
    instructor = None
    lecture = None

    def setUp(self):
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.instructor = Instructor.objects.create(user=temp)
        self.instructor.save()

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmpcourse.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()

        tempsection = SectionObj(hold_section)
        self.lecture = LectureObj(tempsection)

    def test_none_to_remove(self):
        with self.assertRaises(RuntimeError, msg="removeInstr() Tried to remove from none"):
            self.lecture.removeInstr()
    def test_remove(self):
        self.lecture.removeInstr()
        self.assertIsNone(self.lecture.getLecInstrAsmgt(), "removeInstr() did not remove")
class TestLectureGetLecTAAsgmt(unittest.TestCase):  # Joe
    ta = None
    lecture = None

    def setUp(self):
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmpcourse.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()

        tempsection = SectionObj(hold_section)
        self.lecture = LectureObj(tempsection)

    def test_get_ta_assignment(self):
        self.assertEquals(self.ta, self.lecture.getLectureTAAsgmt(),
                          "getLectureTAAsgmt() does not return correct")
    def test_get_no_ta_assignment(self):
        with self.assertRaises(RuntimeError, msg="getLectureTAAsgmt() Tried to retrieve from none"):
            self.lecture.getLectureTAAsgmt()


class TestLectureAddTA(unittest.TestCase):  # Joe
    ta = None
    lecture = None

    def setUp(self):
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmpcourse.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()

        tempsection = SectionObj(hold_section)
        self.lecture = LectureObj(tempsection)

    def test_add(self):
        self.lecture.addTA(self.ta)
    def test_add_but_full(self):
        self.lecture.addTA(self.ta)
        self.assertIsNotNone(self.lecture.getLectureTAAsgmt(), "getLectureTAAsgmt() Did not add instructor")


class TestLectureRemoveTA(unittest.TestCase):  # Joe
    ta = None
    lecture = None

    def setUp(self):
        temp = User(email_address="test@test.com", password="password", first_name="first", last_name="last",
                    home_address="Your mom's house", phone_number=1234567890)
        temp.save()

        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )
        tmpcourse.save()

        hold_section = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        hold_section.save()

        tempsection = SectionObj(hold_section)
        self.lecture = LectureObj(tempsection)
    def test_none_to_remove(self):
        with self.assertRaises(RuntimeError, msg="removeTA() Tried to remove from none"):
            self.lecture.removeTA()
    def test_remove(self):
        self.lecture.removeTA()
        self.assertIsNone(self.lecture.getLectureTAAsgmt(), "removeTA() did not remove")