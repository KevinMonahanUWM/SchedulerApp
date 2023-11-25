import unittest
import datetime

from django.test import TestCase

from TAScheduler.models import Course, User, TA, Section, Lab, Instructor, Lecture
from TAScheduler.views_methods import LabObj, LectureObj, TAObj


# PBI Assignments ...
# Alec = #1,#2 (Total = 6)
# Kevin = #3,#4,#5 (Total = 4)
# Randall = #6,#7,#8 (Total = 12)
# Kiran = #9,#10,#11 (Total = 15)
# Joe = #12,#13 (Total = 8)
# SEE METHOD DESCRIPTIONS FOR GUIDE ON HOW TO WRITE.
# Feel free to make suggestions on discord (add/remove/edit methods)!.
# Remember: These methods were made before any coding (I was guessing) so it's likely they should be changed.
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


class TestSectionGetID(TestCase):  # Joe
    lab = None
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

        tmpsection = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        self.lab = LabObj(tmpsection)

    def test_get_id(self):
        self.assertEquals(self.lab.getID(), 1011, "getID() did not retrieve correct section_id")

    def test_get_but_no_id(self):
        tmpsection = Section.objects.create(
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        self.lab = LabObj(tmpsection)
        self.assertIsNone(self.lab.getID(), "getID() returns an ID when none assigned")

    # Maybe test for section_id = None, but I don't think section can be made without


class TestSectionGetParentCourse(TestCase):  # Joe
    lab = None
    course = None

    # noinspection DuplicatedCode
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

        tmpsection = Section.objects.create(
            section_id=1011,
            course=self.course,
            location="Cool place",
            meeting_time=datetime.datetime
        )
        self.lab = LabObj(tmpsection)

    def test_get_parent_course(self):
        self.assertEquals(self.lab.getParentCourse(), self.course,
                          "getParentCourse() did not retrieve correct course")


class TestLabInit(TestCase):
    lab = None
    info = None
    tempLab = None

    # noinspection DuplicatedCode
    def setUp(self):
        tempuser = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpta = TA.objects.create(
            user=tempuser,
            grader_status=True
        )

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        self.tmplab = Lab.objects.create(
            section=tmpsection,
            ta=tmpta
        )

        self.lab = LabObj(self.tmplab)

    def test_lab_make(self):
        self.assertIsNotNone(self.lab, "__init__ failed in making Lab")

    def test_bad_lab_make(self):
        with self.assertRaises(TypeError, msg="__init__ failed in making Lab, bad input"):
            LabObj(5)


class TestLabGetLabTAAsgmt(TestCase):  # Joe
    lab = None
    ta = None

    # noinspection DuplicatedCode
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

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        self.lab = Lab.objects.create(
            section=tmpsection
        )

    def test_get_ta(self):
        temp = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp.save()
        self.ta = TA.objects.create(user=temp)
        self.ta.save()

        self.lab.ta = self.ta
        self.lab.save()

        self.labObj = LabObj(self.lab)  # Form lab after adding TA manually

        self.assertEquals(
            self.ta,
            self.labObj.getLabTAAsgmt(),
            "getLabTAAsgmt() does not retrieve correct ta; Test may also be accepting wrong object")

    def test_get_but_no_ta(self):
        self.labObj = LabObj(self.lab)  # Form lab with no TA

        self.assertIsNone(self.labObj.getLabTAAsgmt(), "getLabTAAsgmt() finds something with no TA")


class TestLabAddTA(TestCase):  # Joe
    lab = None
    ta = None

    # noinspection DuplicatedCode
    def setUp(self):
        tempuser = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        self.ta = TA.objects.create(
            user=tempuser,
            grader_status=True
        )
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

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmplab = Lab.objects.create(
            section=tmpsection,
        )

        self.lab = LabObj(tmplab)

    def test_add_ta(self):
        self.lab.addTA(TAObj(self.ta))
        self.assertEquals(self.ta, self.lab.getLabTAAsgmt(),
                          "addTA() does not add TA to lab")

    def test_add_ta_but_full(self):
        temp2 = User(email_address="test2@test.com", password="password2", first_name="first2", last_name="last2",
                     home_address="Your mom's house", phone_number=1234567890)

        tempta = TA.objects.create(user=temp2)
        self.lab.addTA(TAObj(self.ta))
        with self.assertRaises(RuntimeError, msg="Tried to add TA to full Lab"):
            self.lab.addTA(TAObj(self.ta))


class TestLabRemoveTA(TestCase):  # Joe
    lab = None
    ta = None

    def setUp(self):
        tempuser = User(
            email_address="test@test.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpta = TA.objects.create(
            user=tempuser,
            grader_status=True
        )

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmplab = Lab.objects.create(
            section=tmpsection,
            ta=tmpta
        )

        self.lab = LabObj(tmplab)

    def test_remove(self):
        self.lab.removeTA()
        self.assertIsNone(self.lab.getLabTAAsgmt(), "removeTA() does not remove TA from lab")

    def test_none_to_remove(self):
        self.lab.removeTA()
        with self.assertRaises(RuntimeError, msg="Tried to remove TA when none in lab"):
            self.lab.removeTA()


class TestLectureInit(TestCase):
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        tempuser = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpta = TA.objects.create(
            user=tempuser,
            grader_status=True
        )

        tempuser2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="firstin",
            last_name="lastin",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpinstructor = Instructor.objects.create(
            user=tempuser2
        )

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        self.lecture = Lecture.objects.create(
            section=tmpsection,
            ta=tmpta,
            instructor=tmpinstructor
        )

    def test_lecture_make(self):
        self.assertIsNotNone(LectureObj(self.lecture), "__init__ failed in making Lecture")

    def test_bad_lecture_make(self):
        with self.assertRaises(TypeError, msg="__init__ failed in making Lecture: Type error"):
            self.lecture = LectureObj(7)


class TestLectureGetLecInstrAsgmt(unittest.TestCase):  # Joe
    instructor = None
    lecture = None

    def setUp(self):
        tempuser = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpta = TA.objects.create(
            user=tempuser,
            grader_status=True
        )

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmplec = Lecture.objects.create(
            section=tmpsection,
            ta=tmpta
        )

        tempuser2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="firstin",
            last_name="lastin",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        self.instructor = Instructor.objects.create(
            user=tempuser2
        )
        self.instructor.save()

        self.lecture = LectureObj(tmplec)

    def test_get_instructor(self):
        self.lecture.addInstr(self.instructor)
        self.assertEquals(self.instructor, self.lecture.getLecInstrAsmgt(),
                          "getLecInstrAsmgt() does not return correct")

    def test_get_with_no_instructor(self):
        self.assertIsNone(self.lecture.getLecInstrAsmgt(), "getLecInstrAsmgt() Retrieved instructor when none exists")


class TestLectureAddInstructor(unittest.TestCase):  # Joe
    lecture = None
    instructor = None

    def setUp(self):
        tempuser2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="firstin",
            last_name="lastin",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        self.instructor = Instructor.objects.create(
            user=tempuser2
        )
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

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmplec = Lecture.objects.create(
            section=tmpsection
        )

        self.info = {
            "section", tmpsection,
        }

        self.lecture = LectureObj(tmplec)

    def test_add_but_full(self):
        self.lecture.addInstr(self.instructor)
        with self.assertRaises(RuntimeError, msg="Tried to add Instructor to full lecture"):
            self.lecture.addInstr(self.instructor)

    def test_add(self):
        self.lecture.addInstr(self.instructor)
        self.assertEquals(
            self.lecture.getLecInstrAsmgt(),
            self.instructor,
            "getLecInstrAsmgt() Did not add instructor to lecture"
        )


class TestLectureRemoveInstructor(unittest.TestCase):  # Joe
    instructor = None
    lecture = None

    def setUp(self):
        tempuser = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpta = TA.objects.create(
            user=tempuser,
            grader_status=True
        )

        tempuser2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="firstin",
            last_name="lastin",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpinstructor = Instructor.objects.create(
            user=tempuser2
        )

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmplec = Lecture.objects.create(
            section=tmpsection,
            ta=tmpta,
            instructor=tmpinstructor
        )

        self.lecture = LectureObj(tmplec)

    def test_none_to_remove(self):
        self.lecture.removeInstr()
        with self.assertRaises(RuntimeError, msg="removeInstr() Tried to remove from lecture with no instructor"):
            self.lecture.removeInstr()

    def test_remove(self):
        self.lecture.removeInstr()
        self.assertIsNone(self.lecture.getLecInstrAsmgt(), "removeInstr() did not remove from lecture")


class TestLectureGetLecTAAsgmt(unittest.TestCase):  # Joe
    ta = None
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        tempuser = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        self.ta = TA.objects.create(
            user=tempuser,
            grader_status=True
        )
        self.ta.save()

        tempuser2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="firstin",
            last_name="lastin",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpinstructor = Instructor.objects.create(
            user=tempuser2
        )

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmplec = Lecture.objects.create(
            section=tmpsection,
            ta=self.ta,
            instructor=tmpinstructor
        )

        self.lecture = LectureObj(tmplec)

    def test_get_ta_assignment(self):
        self.assertEquals(
            self.lecture.getLectureTAAsgmt(),
            self.ta,
            "getLectureTAAsgmt() Retrieved incorrect TA from lecture"
        )

    def test_get_no_ta_assignment(self):
        self.lecture.removeTA()
        self.assertIsNone(
            self.lecture.getLectureTAAsgmt(),
            "getLectureTAAsgmt() retrieved a TA from lecture when none exists"
        )


class TestLectureAddTA(unittest.TestCase):  # Joe
    ta = None
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        tempuser = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpta = TA.objects.create(
            user=tempuser,
            grader_status=True
        )
        self.ta = TAObj(tmpta)

        tempuser2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="firstin",
            last_name="lastin",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpinstructor = Instructor.objects.create(
            user=tempuser2
        )

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmplec = Lecture.objects.create(
            section=tmpsection,
            ta=self.ta,
            instructor=tmpinstructor
        )

        self.lecture = LectureObj(tmplec)

    def test_add(self):
        self.lecture.addTA(self.ta)
        self.assertEquals(self.lecture.getLectureTAAsgmt(), self.ta, "addTA() did not add correct TA to lecture")

    def test_add_but_full(self):
        self.lecture.addTA(self.ta)
        with self.assertRaises(RuntimeError, msg="addTA() Tried to add to full lecture"):
            self.lecture.addTA(self.ta)


class TestLectureRemoveTA(unittest.TestCase):  # Joe
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        tempuser = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpta = TA.objects.create(
            user=tempuser,
            grader_status=True
        )

        tempuser2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="firstin",
            last_name="lastin",
            home_address="Your mom's house",
            phone_number=1234567890
        )

        tmpinstructor = Instructor.objects.create(
            user=tempuser2
        )

        tmpcourse = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online",
            credits=3
        )

        tmpsection = Section.objects.create(
            section_id=1011,
            course=tmpcourse,
            location="Cool place",
            meeting_time=datetime.datetime
        )

        tmplec = Lecture.objects.create(
            section=tmpsection,
            ta=tmpta,
            instructor=tmpinstructor
        )

        self.info = {
            "ta", tmpta,
            "section", tmpsection,
            "instructor", tmpinstructor
        }

        self.lecture = LectureObj(tmplec)

    def test_none_to_remove(self):
        self.lecture.removeTA()
        with self.assertRaises(RuntimeError, msg="removeTA() Tried to remove from none from lecture"):
            self.lecture.removeTA()

    def test_remove(self):
        self.lecture.removeTA()
        self.assertIsNone(self.lecture.getLectureTAAsgmt(), "removeTA() did not remove from lecture")
