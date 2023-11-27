import abc
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from TAScheduler.models import Administrator, User, TA, Instructor, Course, Lecture, Section, Lab


class UserObj(abc.ABC):

    @abc.abstractmethod
    def login(self, email_address, password):
        try:
            User.objects.get(email_address=email_address, password=password)  # Correct field name\
            return True
        except User.DoesNotExist:
            return False  # display "Invalid username or password."

    @abc.abstractmethod
    def getUsername(self):
        return self.user.email_address

    @abc.abstractmethod
    def getPassword(self):
        return self.user.password

    @abc.abstractmethod
    def getName(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @abc.abstractmethod
    def getRole(self):
        if Administrator.objects.filter(user=self.user).exists():
            return "admin"
        if Instructor.objects.filter(user=self.user).exists():
            return "instructor"
        return "ta"


class AdminObj(UserObj):
    admin_database = None

    def __init__(self, admin_info):
        super().__init__()
        if type(admin_info) is not Administrator:
            raise TypeError("Data passed to init method is not a member of the Administrator database class")
        elif not User.objects.filter(email_address=admin_info.user.email_address).exists():
            raise TypeError("The administrator object does not exist in the database")
        self.admin_database = admin_info

    def getUsername(self):
        return self.admin_database.user.email_address

    def getPassword(self):
        return self.admin_database.user.password

    def getName(self):
        return self.admin_database.user.first_name + " " + self.admin_database.user.last_name

    def getRole(self):
        return 'admin'

    def login(self, username, password):
        return super().login(username, password)

    def createCourse(self, course_info):
        if Course.objects.filter(course_id=course_info.get('course_id')).exists():
            raise RuntimeError("Course with this ID already exists")
        new_course = Course.objects.create(**course_info)
        return new_course

    def createUser(self, user_info, role):
        if User.objects.filter(email_address=user_info['email_address']).exists():
            raise RuntimeError("User with this email address already exists")
        new_user = User.objects.create(
            email_address=user_info['email_address'],
            password=user_info['password'],
            first_name=user_info['first_name'],
            last_name=user_info['last_name'],
            home_address=user_info['home_address'],
            phone_number=user_info['phone_number']
        )
        if role.lower() == 'administrator':
            Administrator.objects.create(user=new_user)
        elif role.lower() == 'ta':
            TA.objects.create(user=new_user, grader_status=False)
        elif role.lower() == 'instructor':
            Instructor.objects.create(user=new_user)
        return new_user

    def createSection(self, section_info):
        if Section.objects.filter(section_id=section_info.get('section_id')).exists():
            raise RuntimeError("Section with this ID already exists")
        new_section = Section.objects.create(**section_info)
        return new_section

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
    course_database = None

    def __init__(self, course_info):
        if type(course_info) is not Course:
            raise TypeError("Data passed to init method is not a member of the course database class")
        elif not Course.objects.filter(course_id=course_info.course_id).exists():
            raise TypeError("The course object does not exist in the database")
        self.course_database = course_info

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
