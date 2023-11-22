import unittest

from TAScheduler.models import Course
from TAScheduler.views_methods import CourseObj


# PBI Assignments ...
# Alec = #1,#2 (Total = 6)
# Kevin = #3,#4,#5 (Total = 4)
# Randall = #6,#7,#8 (Total = 12)
# Kiran = #9,#10,#11 (Total = 15)
# Joe = #12,#13 (Total = 8)
# SEE METHOD DESCRIPTIONS FOR GUIDE ON HOW TO WRITE.
# Feel free to make suggestions on discord (add/remove/edit methods)!.
### Rememeber: These methods were made before any coding (I was guessing) so it's likely they should be changed.
class TestUserLogin(unittest.TestCase):  # Alec
    pass


class TestUserGetID(unittest.TestCase):  # Alec
    pass


class TestUserGetPassword(unittest.TestCase):  # Alec
    pass


class TestUserGetName(unittest.TestCase):  # Alec
    pass


class TestUserGetRole(unittest.TestCase):  # Alec
    pass


class TestAdminInit(unittest.TestCase):
    pass

class TestAdminCreateCourse(unittest.TestCase):  # Alec
    pass


class TestAdminCreateUser(unittest.TestCase):  # Alec
    pass


class TestAdminCreateSection(unittest.TestCase):  # Alec
    pass


class TestAdminRemoveCourse(unittest.TestCase):  # Kevin
    tempCourse = None

    def setUp(self):
        hold_course = Course(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )
        hold_course.save()
        self.tempCourse = CourseObj(hold_course)


class TestAdminRemoveAccount(unittest.TestCase):  # Kevin
    pass


class TestAdminRemoveSection(unittest.TestCase):  # Kevin
    pass


class TestAdminEditCourse(unittest.TestCase):  # Kevin
    pass


class TestAdminEditSection(unittest.TestCase):  # Kevin
    pass


class TestAdminEditAccount(unittest.TestCase):  # Kevin
    pass


class TestAdminCourseInstrAsgmt(unittest.TestCase):  # Kevin
    pass


class TestAdminCourseTAAsgmt(unittest.TestCase):  # Kevin
    pass

class TestTAInit(unittest.TestCase):
    pass

class TestTAHasMaxAsgmts(unittest.TestCase):  # Kiran
    pass


class TestTAAssignTACourse(unittest.TestCase):  # Kiran
    pass


class TestTAGetTACrseAsgmts(unittest.TestCase):  # Kiran
    pass


class TestAssignTALab(unittest.TestCase):
    pass


class TestTAGetTALabAsgmts(unittest.TestCase):  # Kiran
    pass


class TestAssignTALec(unittest.TestCase):
    pass


class TestTAGetTALecAsgmts(unittest.TestCase):  # Kiran
    pass


class TestTAGetGraderStatus(unittest.TestCase):  # Kiran
    pass

class TestInstrutorInit(unittest.TestCase):
    pass


class TestInstructorHasMaxAsgmts(unittest.TestCase):  # Kiran
    pass


class TestInstructorAssignInstrCourse(unittest.TestCase):  # Kiran
    pass


class TestInstructorGetInstrCrseAsgmts(unittest.TestCase):  # Kiran
    pass


class TestInstructorAssignInstrLec(unittest.TestCase):  # Kiran
    pass


class TestInstructorGetInstrLecAsgmts(unittest.TestCase):  # Kiran
    pass


class TestInstructorLecTAAsmgt(unittest.TestCase):
    pass


class TestInstructorLabTAAsmgt(unittest.TestCase):
    pass

class TestCourseInit(unittest.TestCase):
    pass


class TestCourseAddInstructor(unittest.TestCase):  # Randall
    pass


class TestCourseAddTA(unittest.TestCase):  # Randall
    pass


class TestCourseRemoveAssignment(unittest.TestCase):  # Randall
    pass


class TestCourseRemoveCourse(unittest.TestCase):  # Randall
    pass


class TestCourseEditCourseInfo(unittest.TestCase):  # Randall
    pass


class TestCourseGetAsgmtsForCrse(unittest.TestCase):  # Randall
    pass


class TestCourseGetSectionsForCrse(unittest.TestCase):  # Randall
    pass


class TestCourseGetCrseInfo(unittest.TestCase):  # Randall
    pass


class TestSectionGetID(unittest.TestCase):  # Joe
    pass


class TestSectionGetParentCourse(unittest.TestCase):  # Joe
    pass


class TestLabInit(unittest.TestCase):
    pass

class TestLabGetLabTAAsgmt(unittest.TestCase):  # Joe
    pass


class TestLabAddTA(unittest.TestCase):  # Joe
    pass


class TestLabRemoveTA(unittest.TestCase):  # Joe
    pass


class TestLectureInit(unittest.TestCase):
    pass

class TestLectureGetLecInstrAsgmt(unittest.TestCase):  # Joe
    pass


class TestLectureAddInstructor(unittest.TestCase):  # Joe
    pass


class TestLectureRemoveInstructor(unittest.TestCase):  # Joe
    pass


class TestLectureGetLecTAAsgmt(unittest.TestCase):  # Joe
    pass


class TestLectureAddTA(unittest.TestCase):  # Joe
    pass


class TestLectureRemoveTA(unittest.TestCase):  # Joe
    pass
