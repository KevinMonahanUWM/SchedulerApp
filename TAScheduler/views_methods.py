import abc


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

    def __init__(self, admin_info):
        pass

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

    def __init__(self, ta_info):
        pass

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
    databaseReference = None

    def __init__(self, instr_info):
        pass

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

    def __init__(self, course_info):
        pass

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

    def __init__(self, lec_info):
        pass

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

    def __init__(self, lab_info):
        pass

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
