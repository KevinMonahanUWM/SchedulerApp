from django.test import TestCase

from TAScheduler.models import Course, User
from TAScheduler.views_methods import CourseObj, AdminObj


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


class Admin:
    pass


class TestAdminRemoveCourse(TestCase):  # Kevin
    tempCourse = None
    admin = None
    hold_course = None

    def setUp(self):
        self.hold_course = Course.objects.create(
            course_id=101,
            semester='Fall 2023',
            name='Introduction to Testing',
            description='A course about writing tests in Django.',
            num_of_sections=3,
            modality='Online',
            credits=4
        )
        self.tempCourse = CourseObj(self.hold_course)
        hold_user = User(
            email_address='admin@example.com',
            password='adminpassword',
            first_name='Admin',
            last_name='User',
            home_address='123 Admin St',
            phone_number='1234567890'
        )
        hold_user.save()
        hold_admin = Admin(user=hold_user)
        hold_admin.save()
        self.admin = AdminObj(hold_admin)

    def test_successful_delete(self):
        self.admin.removeCourse(self.tempCourse)
        self.assertNotIn(Course.objects, self.hold_course, "Did not remove course from ")

    def test_delete_null_course(self):
        Course.delete(self.hold_course)
        with self.assertRaises(RuntimeError, msg="Tried to delete a non-existent course"):
            self.admin.removeCourse(self.tempCourse)

    def test_delete_non_course(self):
        with self.assertRaises(TypeError, msg="Tried to delete not a course"):
            self.admin.removeCourse(11)


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
    pass


class TestSectionGetParentCourse(TestCase):  # Joe
    pass


class TestLabInit(TestCase):
    pass


class TestLabGetLabTAAsgmt(TestCase):  # Joe
    pass


class TestLabAddTA(TestCase):  # Joe
    pass


class TestLabRemoveTA(TestCase):  # Joe
    pass


class TestLectureInit(TestCase):
    pass


class TestLectureGetLecInstrAsgmt(TestCase):  # Joe
    pass


class TestLectureAddInstructor(TestCase):  # Joe
    pass


class TestLectureRemoveInstructor(TestCase):  # Joe
    pass


class TestLectureGetLecTAAsgmt(TestCase):  # Joe
    pass


class TestLectureAddTA(TestCase):  # Joe
    pass


class TestLectureRemoveTA(TestCase):  # Joe
    pass
