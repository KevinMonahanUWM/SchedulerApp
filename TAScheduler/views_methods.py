import abc

from TAScheduler.models import Administrator, User, TA, Instructor, Course, Lecture, Section, Lab, InstructorToCourse, \
    TAToCourse


class UserObj(abc.ABC):

    @abc.abstractmethod
    def login(self, username, password):
        pass

    @abc.abstractmethod
    def getUsername(self):
        pass

    @abc.abstractmethod
    def getPassword(self):
        pass

    @abc.abstractmethod
    def getName(self):
        pass

    @abc.abstractmethod
    def getRole(self):
        pass


class AdminObj(UserObj):
    admin_database = None

    def __init__(self, admin_info):
        if type(admin_info) is not Administrator:
            raise TypeError("Data passed to init method is not a member of the Administrator database class")
        elif not User.objects.filter(email_address=admin_info.user.email_address).exists():
            raise TypeError("The administrator object does not exist in the database")
        self.admin_database = admin_info

    def getUsername(self):
        pass

    def getPassword(self):
        pass

    def getName(self):
        pass

    def getRole(self):
        pass

    def login(self, username, password):
        pass

    def createCourse(self, course_info):
        pass

    def createUser(self, user_info):
        pass

    def createSection(self, section_info):
        pass

    def removeCourse(self, active_course):
        pass

    def removeUser(self, active_user):
        pass

    def removeSection(self, active_section):
        pass

    def editCourse(self, active_course, new_info):  # new inputs
        pass

    def editSection(self, active_section, new_info):  # new inputs
        pass

    def editUser(self, active_user, new_info):  # new inputs
        pass

    def courseInstrAsmgt(self, active_instr, active_course):  # new inputs
        pass

    def courseTAAsmgt(self, active_ta, active_course):  # new remove sectionTAAsmgt
        pass


class TAObj(UserObj):
    ta_database = None

    def __init__(self, ta_info):
        if type(ta_info) is not TA:
            raise TypeError("Data passed to init method is not a member of the TA database class")
        elif not User.objects.filter(email_address=ta_info.user.email_address).exists():
            raise TypeError("The ta object does not exist in the database")
        self.ta_database = ta_info

    def login(self, username, password):
        pass

    def getUsername(self):
        pass

    def getPassword(self):
        pass

    def getName(self):
        pass

    def getRole(self):
        pass

    def hasMaxAsgmts(self):
        pass

    def assignTACourse(self, active_course):
        pass

    def assignTALab(self, active_lab):
        pass

    def assignTALecture(self, active_lecture):  # new
        pass

    def getTACrseAsgmts(self):
        pass

    def getTALabAsgmts(self):
        pass

    def getTALecAsgmts(self):  # new
        pass

    def getGraderStatus(self):
        pass


class InstructorObj(UserObj):
    instr_database = None

    def __init__(self, instr_info):
        if type(instr_info) is not Instructor:
            raise TypeError("Data passed to init method is not a member of the Instructor database class")
        elif not User.objects.filter(email_address=instr_info.user.email_address).exists():
            raise TypeError("The instructor object does not exist in the database")
        self.instr_database = instr_info

    def login(self, username, password):
        pass

    def getUsername(self):
        pass

    def getPassword(self):
        pass

    def getName(self):
        pass

    def getRole(self):
        pass

    def hasMaxAsgmts(self):
        pass

    def assignInstrCourse(self, active_course):
        pass

    def assignInstrLecture(self, active_lecture):  # new
        pass

    def getInstrCrseAsgmts(self):
        pass

    def getInstrLecAsgmts(self):  # new
        pass

    def lecTAAsmgt(self, active_ta, active_lecture):  # new
        pass

    def labTAAsmgt(self, active_ta, active_lab):  # new
        pass


class CourseObj:
    course_database = None

    def __init__(self, course_info):
        if type(course_info) is not Course:
            raise TypeError("Data passed to init method is not a member of the course database class")
        elif not Course.objects.filter(course_id=course_info.course_id).exists():
            raise TypeError("The course object does not exist in the database")
        self.course_database = course_info

    def addInstructor(self, active_instr):
        if not isinstance(active_instr, InstructorObj):
            raise TypeError("active_instr is not an instance of InstructorObj")
        if not active_instr.instr_database.user_id:
            raise ValueError("Instructor must have a valid user associated")

        if InstructorToCourse.objects.filter(instructor=active_instr.instr_database,
                                             course=self.course_database).exists():
            raise ValueError("Instructor is already assigned to this course")

        if InstructorToCourse.objects.filter(
                instructor=active_instr.instr_database).count() >= active_instr.instr_database.max_assignments:
            raise ValueError("Instructor has reached the maximum number of course assignments")

        if InstructorToCourse.objects.filter(
                course=self.course_database).count() >= self.course_database.num_of_sections:
            raise ValueError(
                "This course has reached the maximum number of instructors based on the number of sections")
        if not Instructor.objects.filter(id=active_instr.instr_database.id).exists():
            raise ValueError("Instructor must be saved in the database before being assigned to a course")

        InstructorToCourse.objects.create(instructor=active_instr.instr_database, course=self.course_database)

    def addTa(self, active_ta):
        if not isinstance(active_ta, TAObj):
            raise TypeError("active_ta is not an instance of TAObj")

        if TAToCourse.objects.filter(ta=active_ta.ta_database, course=self.course_database).exists():
            raise ValueError("TA is already assigned to this course")

        if TAToCourse.objects.filter(ta=active_ta.ta_database).count() >= active_ta.ta_database.max_assignments:
            raise ValueError("TA has reached the maximum number of course assignments")

        if TAToCourse.objects.filter(course=self.course_database).count() >= self.course_database.num_of_sections:
            raise ValueError("This course has reached the maximum number of TAs based on the number of sections")

        TAToCourse.objects.create(ta=active_ta.ta_database, course=self.course_database)

    def removeAssignment(self, active_user):
        # to implement a way to determine if a user is a TA or Instructor
        if isinstance(active_user, InstructorObj):
            InstructorToCourse.objects.filter(
                course=self.course_database,
                instructor=active_user.instr_database  # Corrected attribute name
            ).delete()
        elif isinstance(active_user, TAObj):
            TAToCourse.objects.filter(
                course=self.course_database,
                ta=active_user.ta_database  # Corrected attribute name
            ).delete()
        else:
            raise TypeError("The active_user must be an instance of InstructorObj or TAObj")

    def removeCourse(self):
        self.course_database.delete()

    def editCourse(self, course_info):
        for attr, value in course_info.items():
            setattr(self.course_database, attr, value)
        self.course_database.full_clean()  # call the model's clean() method to validate the fields.
        self.course_database.save()

    def getAsgmtsForCrse(self):
        instructor_assignments = InstructorToCourse.objects.filter(course=self.course_database)
        ta_assignments = TAToCourse.objects.filter(course=self.course_database)
        return {
            'instructors': list(instructor_assignments),
            'tas': list(ta_assignments)
        }

    def getSectionsCrse(self):
        return list(Section.objects.filter(course=self.course_database))

    def getCrseInfo(self):
        return {
            'course_id': self.course_database.course_id,
            'semester': self.course_database.semester,
            'name': self.course_database.name,
            'description': self.course_database.description,
            'num_of_sections': self.course_database.num_of_sections,
            'modality': self.course_database.modality,
            'credits': self.course_database.credits
        }


class SectionObj(abc.ABC):

    @abc.abstractmethod
    def getID(self):
        pass

    @abc.abstractmethod
    def getParentCourse(self):
        pass


class LectureObj(SectionObj):
    lecture_database = None

    def __init__(self, lecture_info):
        if type(lecture_info) is not Lecture:
            raise TypeError("Data passed to init method is not a member of the lecture database class")
        elif not Section.objects.filter(section_id=lecture_info.section.section_id).exists():
            raise TypeError("The lecture object does not exist in the database")
        self.lecture_database = lecture_info

    def getID(self):
        pass

    def getParentCourse(self):
        pass

    def getLectureTAAsgmt(self):  # new
        pass

    def addTA(self, active_ta):  # new
        pass

    def getLecInstrAsmgt(self):
        pass

    def addInstr(self, active_instr):
        pass

    def removeInstr(self):
        pass

    def removeTA(self):  # new
        pass


class LabObj(SectionObj):
    lab_database = None

    def __init__(self, lab_info):
        if type(lab_info) is not Lab:
            raise TypeError("Data passed to init method is not a member of the lab database class")
        elif not Section.objects.filter(section_id=lab_info.section.section_id).exists():
            raise TypeError("The lab object does not exist in the database")
        self.lab_database = lab_info

    def getID(self):
        pass

    def getParentCourse(self):
        pass

    def getLabTAAsgmt(self):
        pass

    def addTA(self, active_ta):
        pass

    def removeTA(self):
        pass
