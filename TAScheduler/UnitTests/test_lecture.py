from django.test import TestCase
from TAScheduler.models import User, Instructor, Course, TA, Section, Lecture
from TAScheduler.views_methods import LectureObj


class TestLectureInit(TestCase):
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        self.lecture = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta,
            instructor=tmp_instructor
        )
        self.lecture.save()

    def test_lecture_make(self):
        self.assertIsNotNone(LectureObj(self.lecture), "__init__ failed in making Lecture")

    def test_bad_lecture_make(self):
        with self.assertRaises(TypeError, msg="__init__ failed in making Lecture: Type error"):
            self.lecture = LectureObj(7)


class TestLectureGetLecInstrAssignment(TestCase):  # Joe
    instructor = None
    lecture = None

    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta
        )
        tmp_lec.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        self.instructor = Instructor.objects.create(
            user=temp_user2
        )
        self.instructor.save()

        self.lecture = LectureObj(tmp_lec)

    def test_get_instructor(self):
        self.lecture.addInstr(self.instructor)
        self.assertEqual(self.instructor, self.lecture.getLecInstrAsmgt(),
                          "getLecInstrAssignment() does not return correct")

    def test_get_with_no_instructor(self):
        self.assertIsNone(self.lecture.getLecInstrAsmgt(),
                          "getLecInstrAssignment() Retrieved instructor when none exists")


class TestLectureAddInstructor(TestCase):  # Joe
    lecture = None
    instructor = None

    def setUp(self):
        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        self.instructor = Instructor.objects.create(
            user=temp_user2
        )
        self.instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section
        )
        tmp_lec.save()

        self.info = {
            "section", tmp_section,
        }

        self.lecture = LectureObj(tmp_lec)

    def test_add_but_full(self):
        self.lecture.addInstr(self.instructor)
        with self.assertRaises(RuntimeError, msg="Tried to add Instructor to full lecture"):
            self.lecture.addInstr(self.instructor)

    def test_add(self):
        self.lecture.addInstr(self.instructor)
        self.assertEqual(
            self.lecture.getLecInstrAsmgt(),
            self.instructor,
            "getLecInstrAssignment() Did not add instructor to lecture"
        )


# noinspection DuplicatedCode
class TestLectureRemoveInstructor(TestCase):  # Joe
    instructor = None
    lecture = None

    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta,
            instructor=tmp_instructor
        )
        tmp_lec.save()

        self.lecture = LectureObj(tmp_lec)

    def test_none_to_remove(self):
        self.lecture.removeInstr()
        with self.assertRaises(RuntimeError, msg="removeInstr() Tried to remove from lecture with no instructor"):
            self.lecture.removeInstr()

    def test_remove(self):
        self.lecture.removeInstr()
        self.assertIsNone(self.lecture.getLecInstrAsmgt(), "removeInstr() did not remove from lecture")


class TestLectureGetLecTAAssignment(TestCase):  # Joe
    ta = None
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        self.ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        self.ta.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=self.ta,
            instructor=tmp_instructor
        )
        tmp_lec.save()

        self.lecture = LectureObj(tmp_lec)

    def test_get_ta_assignment(self):
        self.assertEqual(
            self.lecture.getLectureTAAsgmt(),
            self.ta,
            "getLectureTAAssignment() Retrieved incorrect TA from lecture"
        )

    def test_get_no_ta_assignment(self):
        self.lecture.removeTA()
        self.assertIsNone(
            self.lecture.getLectureTAAsgmt(),
            "getLectureTAAssignment() retrieved a TA from lecture when none exists"
        )


class TestLectureAddTA(TestCase):  # Joe
    ta = None
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()
        self.ta = tmp_ta

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            instructor=tmp_instructor
        )
        tmp_lec.save()

        self.lecture = LectureObj(tmp_lec)

    def test_add(self):
        self.lecture.addTA(self.ta)
        self.assertEqual(self.lecture.getLectureTAAsgmt(), self.ta, "addTA() did not add correct TA to lecture")

    def test_add_but_full(self):
        self.lecture.addTA(self.ta)
        with self.assertRaises(RuntimeError, msg="addTA() Tried to add to full lecture"):
            self.lecture.addTA(self.ta)


class TestLectureRemoveTA(TestCase):  # Joe
    lecture = None

    # noinspection DuplicatedCode
    def setUp(self):
        temp_user = User(
            email_address="test@ta.com",
            password="password",
            first_name="first",
            last_name="last",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user.save()

        tmp_ta = TA.objects.create(
            user=temp_user,
            grader_status=True
        )
        tmp_ta.save()

        temp_user2 = User(
            email_address="test@instructor.com",
            password="password",
            first_name="first_in",
            last_name="last_in",
            home_address="Your mom's house",
            phone_number=1234567890
        )
        temp_user2.save()

        tmp_instructor = Instructor.objects.create(
            user=temp_user2
        )
        tmp_instructor.save()

        tmp_course = Course.objects.create(
            course_id=100,
            semester="fall 2023",
            name="testCourse",
            description="test",
            num_of_sections=3,
            modality="online"
        )
        tmp_course.save()

        tmp_section = Section.objects.create(
            section_id=1011,
            course=tmp_course,
            location="Cool place",
            meeting_time="2000-1-1 12:00:00"
        )
        tmp_section.save()

        tmp_lec = Lecture.objects.create(
            section=tmp_section,
            ta=tmp_ta,
            instructor=tmp_instructor
        )
        tmp_lec.save()

        self.info = {
            "ta", tmp_ta,
            "section", tmp_section,
            "instructor", tmp_instructor
        }

        self.lecture = LectureObj(tmp_lec)

    def test_none_to_remove(self):
        self.lecture.removeTA()
        with self.assertRaises(RuntimeError, msg="removeTA() Tried to remove from none from lecture"):
            self.lecture.removeTA()

    def test_remove(self):
        self.lecture.removeTA()
        self.assertIsNone(self.lecture.getLectureTAAsgmt(), "removeTA() did not remove from lecture")