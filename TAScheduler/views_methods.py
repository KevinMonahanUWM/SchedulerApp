import abc

from TAScheduler.models import Administrator, User, TA, Instructor, Course, Lecture, Section, Lab


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
    database = None

    def __init__(self, admin_info):
        if type(admin_info) is not Administrator:
            raise TypeError("Data passed to init method is not a member of the Administrator database class")
        elif not User.objects.filter(email_address=admin_info.user.email_address).exists():
            raise TypeError("The administrator object does not exist in the database")
        self.database = admin_info

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
    database = None

    def __init__(self, ta_info):
        if type(ta_info) is not TA:
            raise TypeError("Data passed to init method is not a member of the TA database class")
        elif not User.objects.filter(email_address=ta_info.user.email_address).exists():
            raise TypeError("The ta object does not exist in the database")
        self.database = ta_info

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
    database = None

    def __init__(self, instr_info):
        if type(instr_info) is not Instructor:
            raise TypeError("Data passed to init method is not a member of the Instructor database class")
        elif not User.objects.filter(email_address=instr_info.user.email_address).exists():
            raise TypeError("The instructor object does not exist in the database")
        self.database = instr_info

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

    def assignInstrLecture(self, active_lecture):  # new.
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
    database = None

    def __init__(self, course_info):
        if type(course_info) is not Course:
            raise TypeError("Data passed to init method is not a member of the course database class")
        elif not Course.objects.filter(course_id=course_info.course_id).exists():
            raise TypeError("The course object does not exist in the database")
        self.database = course_info

    def addInstructor(self, active_instr):
        pass

    def addTa(self, active_ta):
        pass

    def removeAssignment(self, active_user):
        pass

    def removeCourse(self):
        pass

    def editCourse(self, course_info):
        pass

    def getAsgmtsForCrse(self):
        pass

    def getSectionsCrse(self):
        pass

    def getCrseInfo(self):
        pass


class SectionObj(abc.ABC):

    @abc.abstractmethod
    def getID(self):
        pass

    @abc.abstractmethod
    def getParentCourse(self):
        pass


class LectureObj(SectionObj):
    database = None

    def __init__(self, lecture_info):
        if type(lecture_info) is not Lecture:
            raise TypeError("Data passed to init method is not a member of the lecture database class")
        elif not Section.objects.filter(section_id=lecture_info.section.section_id).exists():
            raise TypeError("The lecture object does not exist in the database")
        self.database = lecture_info

    def getID(self):
        return self.database.section.section_id

    def getParentCourse(self):
        return self.database.section.course

    def getLectureTAAsgmt(self):  # new
        return self.database.ta

    def addTA(self, active_ta):  # new
        if type(active_ta) is not TA:
            raise TypeError("Data passed to addTA method is not a TA")
        elif not TA.objects.filter(user=active_ta.user).exists():
            raise TypeError("The TA object does not exist in the database")
        elif self.database.ta is not None:
            raise RuntimeError("A TA already exists")
        self.database.ta = active_ta

    def getLecInstrAsmgt(self):
        return self.database.instructor

    def addInstr(self, active_instr):
        if type(active_instr) is not Instructor:
            raise TypeError("Data passed to addInstructor method is not a Instructor")
        elif not Instructor.objects.filter(user=active_instr.user).exists():
            raise TypeError("The Instructor object does not exist in the database")
        elif self.database.instructor is not None:
            raise RuntimeError("An Instructor already exists")
        self.database.instructor = active_instr

    def removeInstr(self):
        if self.database.instructor is None:
            raise RuntimeError("No instructor to remove")
        self.database.instructor = None

    def removeTA(self):  # new
        if self.database.ta is None:
            raise RuntimeError("No TA to remove")
        self.database.ta = None


class LabObj(SectionObj):
    database = None

    def __init__(self, lab_info):
        if type(lab_info) is not Lab:
            raise TypeError("Data passed to init method is not a member of the lab database class")
        elif not Section.objects.filter(section_id=lab_info.section.section_id).exists():
            raise TypeError("The lab object does not exist in the database")
        self.database = lab_info

    def getID(self):
        return self.database.section.section_id

    def getParentCourse(self):
        return self.database.section.course

    def getLabTAAsgmt(self):
        return self.database.ta

    def addTA(self, active_ta):
        if type(active_ta) is not TA:
            raise TypeError("Data passed to addTA method is not a TA")
        elif not TA.objects.filter(user=active_ta.user).exists():
            raise TypeError("The TA object does not exist in the database")
        elif self.database.ta is not None:
            raise RuntimeError("A TA already exists")
        self.database.ta = active_ta

    def removeTA(self):
        if self.database.ta is None:
            raise RuntimeError("No TA to remove")
        self.database.ta = None
