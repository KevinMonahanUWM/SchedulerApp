from TAScheduler.models import Instructor, Course, Section, InstructorToCourse, TAToCourse
from TAScheduler.view_methods.instructor_methods import InstructorObj
from TAScheduler.view_methods.ta_methods import TAObj


class CourseObj:
    database = None

    def __init__(self, course_info):
        if type(course_info) is not Course:
            raise TypeError("Data passed to init method is not a member of the course database class")
        elif not Course.objects.filter(course_id=course_info.course_id).exists():
            raise TypeError("The course object does not exist in the database")
        self.database = course_info

    def addInstructor(self, active_instr):
        if not isinstance(active_instr, InstructorObj):
            raise TypeError("active_instr is not an instance of InstructorObj")
        if not active_instr.database.user_id:
            raise ValueError("Instructor must have a valid user associated")

        if InstructorToCourse.objects.filter(instructor=active_instr.database,
                                             course=self.database).exists():
            raise ValueError("Instructor is already assigned to this course")

        if InstructorToCourse.objects.filter(
                instructor=active_instr.database).count() >= active_instr.database.max_assignments:
            raise ValueError("Instructor has reached the maximum number of course assignments")

        if InstructorToCourse.objects.filter(
                course=self.database).count() >= self.database.num_of_sections:
            raise ValueError(
                "This course has reached the maximum number of instructors based on the number of sections")
        if not Instructor.objects.filter(id=active_instr.database.id).exists():
            raise ValueError("Instructor must be saved in the database before being assigned to a course")

        InstructorToCourse.objects.create(instructor=active_instr.database, course=self.database)

    def addTa(self, active_ta):
        if not isinstance(active_ta, TAObj):
            raise TypeError("active_ta is not an instance of TAObj")

        if TAToCourse.objects.filter(ta=active_ta.database, course=self.database).exists():
            raise ValueError("TA is already assigned to this course")

        if TAToCourse.objects.filter(ta=active_ta.database).count() >= active_ta.database.max_assignments:
            raise ValueError("TA has reached the maximum number of course assignments")

        if TAToCourse.objects.filter(course=self.database).count() >= self.database.num_of_sections:
            raise ValueError("This course has reached the maximum number of TAs based on the number of sections")

        TAToCourse.objects.create(ta=active_ta.database, course=self.database)

    def removeAssignment(self, active_user):
        # to implement a way to determine if a user is a TA or Instructor
        if isinstance(active_user, InstructorObj):
            InstructorToCourse.objects.filter(
                course=self.database,
                instructor=active_user.database  # Corrected attribute name
            ).delete()
        elif isinstance(active_user, TAObj):
            TAToCourse.objects.filter(
                course=self.database,
                ta=active_user.database  # Corrected attribute name
            ).delete()
        else:
            raise TypeError("The active_user must be an instance of InstructorObj or TAObj")

    def removeCourse(self):
        self.database.delete()

    def editCourse(self, course_info):
        for attr, value in course_info.items():
            setattr(self.database, attr, value)
        self.database.full_clean()  # call the model's clean() method to validate the fields.
        self.database.save()

    def getAsgmtsForCrse(self):
        instructor_assignments = InstructorToCourse.objects.filter(course=self.database)
        ta_assignments = TAToCourse.objects.filter(course=self.database)
        return {
            'instructors': list(instructor_assignments),
            'tas': list(ta_assignments)
        }

    def getSectionsCrse(self):
        return list(Section.objects.filter(course=self.database))

    def getCrseInfo(self):
        return {
            'course_id': self.database.course_id,
            'semester': self.database.semester,
            'name': self.database.name,
            'description': self.database.description,
            'num_of_sections': self.database.num_of_sections,
            'modality': self.database.modality
        }
