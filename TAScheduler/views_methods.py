import abc

from TAScheduler.models import Administrator, User, TA, Instructor, Course, Lecture, Section, Lab, TAToCourse, \
    InstructorToCourse


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
        if type(active_course) is not CourseObj:
            raise TypeError("Input passed is not a Course object")
        elif not Course.objects.filter(course_id=active_course.course_database.course_id).exists():
            raise RuntimeError("Course does not exist")
        Course.delete(active_course.course_database)

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
            raise TypeError("The user object associated with the TA does not exist in the database")
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
        maxAsgmts = self.ta_database.max_assignments
        actualAsgmts = TAToCourse.objects.filter(ta=self.ta_database).count()
        return (actualAsgmts >= maxAsgmts)  # shouldn't ever be ">" but technically true if so (def can't be false)

    def assignTACourse(self, active_course):  # ADJUSTED TESTS!
        if not isinstance(active_course, CourseObj):
            raise TypeError("Sent in incorrect course type into the AssignTACourse.")
        courseDB = active_course.course_database
        if not Course.objects.filter(course_id=courseDB.course_id).exists():
            raise ValueError("The provided Course object does not have an equivalent record in the database.")
        if TAToCourse.objects.filter(ta=self.ta_database, course=courseDB).exists():
            raise ValueError("Can't assign a course already assigned to this TA.")
        if courseDB.num_of_sections == TAToCourse.objects.filter(course=courseDB).count():
            raise ValueError("Can't assign course that has reached it's maximum assignments")
        if self.hasMaxAsgmts():  # not sure what error this is
            raise ValueError("Can't assign a course past a TA's maximum capacity")

        TAToCourse(course=courseDB,ta=self.ta_database).save()  # Assign the course? Is that it?
#
    def assignTALab(self, active_lab): 
        if not isinstance(active_lab, LabObj):
            raise TypeError("Sent in incorrect lab type into the AssignTALab.")
        if self.ta_database.grader_status:
            raise RuntimeError("Can't assign TA a lab with grader status")

        argLabDB = active_lab.lab_database
        if argLabDB.section is None: # SHOULD BE IMPOSSIBLE*
            raise ValueError("The provided Lab object does not have an equivalent section record in the database.")
        if not argLabDB.ta is None:
            raise ValueError("Can't assign a lab that already have a TA.")

        secDB = argLabDB.section
        qs = Lab.objects.filter(section=secDB, ta=self.ta_database)
        if qs.count()>0:
            raise ValueError("Can't assign a lab already assigned to this TA.")

        argLabDB.ta = self.ta_database
        argLabDB.save()  # Assign the lab? Is that it?

    def assignTALecture(self, active_lecture):  # new 
        if not isinstance(active_lecture, LectureObj):
            raise TypeError("Sent in incorrect lecture type into the AssignTALec.")
        if not self.ta_database.grader_status:
            raise RuntimeError("Can't assign TA a lec without grader status")

        argLecDB = active_lecture.lecture_database
        if argLecDB.section is None:  # SHOULD BE IMPOSSIBLE*
            raise ValueError("The provided Lab object does not have an equivalent section record in the database.")
        if not argLecDB.ta is None:
            raise ValueError("Can't assign a lec that already have a TA.")

        argSecDB = argLecDB.section
        qs = Lecture.objects.filter(section=argSecDB, ta=self.ta_database)
        if qs.count()>0:
            raise ValueError("Can't assign a lecture already assigned to this TA.")

        argLecDB.ta = self.ta_database
        argLecDB.save()  # Assign the lec? Is that it?

    def getTACrseAsgmts(self):
        return TAToCourse.objects.filter(ta=self.ta_database)

    def getTALabAsgmts(self):
        return Lab.objects.filter(ta=self.ta_database)

    def getTALecAsgmts(self):  # new
        return Lecture.objects.filter(ta=self.ta_database)

    def getGraderStatus(self):
        return self.ta_database.grader_status


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
        maxAsgmts = self.instr_database.max_assignments
        actualAsgmts = InstructorToCourse.objects.filter(instructor=self.instr_database).count()
        return (actualAsgmts >= maxAsgmts)  # shouldn't ever be ">" but technically true if so (def can't be false)

    def assignInstrCourse(self, active_course):
        if not isinstance(active_course, CourseObj):
            raise TypeError("Sent in incorrect course type into the AssignInstrCourse.")
        courseDB = active_course.course_database
        if not Course.objects.filter(course_id=courseDB.course_id).exists():
            raise ValueError("The provided Course object does not have an equivalent record in the database.")
        if InstructorToCourse.objects.filter(instructor=self.instr_database, course=courseDB).exists():
            raise ValueError("Can't assign a course already assigned to this instructor.")
        if courseDB.num_of_sections == InstructorToCourse.objects.filter(course=courseDB).count():
            raise ValueError("Can't assign course that has reached it's maximum assignments")
        if self.hasMaxAsgmts():  # not sure what error this is
            raise ValueError("Can't assign a course past a instructor's maximum capacity")

        InstructorToCourse(course=courseDB, instructor=self.instr_database).save()

    def assignInstrLecture(self, active_lecture):  # new
        if not isinstance(active_lecture, LectureObj):
            raise TypeError("Sent in incorrect lecture type into the AssignTALec.")

        argLecDB = active_lecture.lecture_database
        if argLecDB.section is None:  # SHOULD BE IMPOSSIBLE*
            raise ValueError("The provided Lab object does not have an equivalent section record in the database.")
        if not argLecDB.instructor is None:
            raise ValueError("Can't assign a lec that already have a instr.")

        argSecDB = argLecDB.section
        qs = Lecture.objects.filter(section=argSecDB, instructor=self.instr_database)
        if qs.count() > 0:
            raise ValueError("Can't assign a lecture already assigned to this instructor.")

        argLecDB.instructor = self.instr_database
        argLecDB.save()  # Assign the lec? Is that it?

    def getInstrCrseAsgmts(self):
        return InstructorToCourse.objects.filter(instructor=self.instr_database)

    def getInstrLecAsgmts(self):  # new
        return Lecture.objects.filter(instructor=self.instr_database)


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
            TypeError("Data passed to init method is not a member of the lecture database class")
        elif not Section.objects.filter(section_id=lecture_info.section.section_id).exists():
            TypeError("The lecture object does not exist in the database")
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
            raise ValueError("The lab object does not exist in the database")
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
