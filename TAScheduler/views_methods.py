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
        return self.database.user.email_address

    def getPassword(self):
        pass

    def getName(self):
        pass

    def getRole(self):
        return type(self.database)

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
        elif not Course.objects.filter(course_id=active_course.database.course_id).exists():
            raise RuntimeError("Course does not exist")
        Course.delete(active_course.database)

    def removeUser(self, active_user):
        if not isinstance(active_user, UserObj):
            raise TypeError("Input passed is not a subclass of userobj")
        elif not User.objects.filter(email_address=active_user.getUsername()).exists():
            raise RuntimeError("User does not exist")
        User.delete(active_user.database.user)

    def removeSection(self, active_section):
        if not isinstance(active_section, SectionObj):
            raise TypeError("Input passed is not a subclass of sectionobj")
        elif not Section.objects.filter(section_id=active_section.getID()).exists():
            raise RuntimeError("Section does not exist")
        Section.delete(active_section.database.section)

    def editCourse(self, active_course, new_info):  # new inputs
        if type(active_course) is not CourseObj:
            raise TypeError("Input passed is not a Course object")
        elif not Course.objects.filter(course_id=active_course.database.course_id).exists():
            raise RuntimeError("Course does not exist")
        if type(new_info) is not dict:
            raise TypeError("Input passed is not a dictionary")

        try:  # Course ID
            if type(new_info.get("course_id")) is not int:
                raise TypeError("Course id expects an int")
            if Course.objects.filter(course_id=new_info.get("course_id")).exists():
                raise RuntimeError("Can not have two courses with the same course number")
            active_course.database.course_id = new_info.get("course_id")
        except KeyError:  # No course_id in list that is fine don't change the database
            active_course.database.course_id = active_course.database.course_id
        try:  # Semester
            if type(new_info.get("semester")) is not str or len(new_info.get("semester")) > 11:
                raise TypeError("semester expects a string")
            if new_info.get("name") == '':
                raise KeyError  # Should go to except section because if string
                # is empty we don't replace the name with nothing
            active_course.database.semester = new_info.get("semester")
        except KeyError:  # No semester in list that is fine don't change the database
            active_course.database.semester = active_course.database.semester
        try:  # Name
            if type(new_info.get("name")) is not str or len(new_info.get("name")) > 100:
                raise TypeError("name expects a string")
            if new_info.get("name") == '':
                raise KeyError  # Should go to except section because if string
                # is empty we don't replace the name with nothing
            active_course.database.name = new_info.get("name")
        except KeyError:  # No name in list that is fine don't change the database
            active_course.database.name = active_course.database.name
        try:  # Description
            if type(new_info.get("description")) is not str or len(new_info.get("description")) > 1000:
                raise TypeError("description expects a string")
            if new_info.get("description") == '':
                raise KeyError  # Should go to except section because if string
                # is empty we don't replace the description with nothing
            active_course.database.description = new_info.get("description")
        except KeyError:  # No description in list that is fine don't change the database
            active_course.database.description = active_course.database.description
        try:  # num_of_sections
            if type(new_info.get("num_of_sections")) is not int:
                raise TypeError("num_of_sections expects an int")
            active_course.database.num_of_sections = new_info.get("num_of_sections")
        except KeyError:  # No num_of_sections in list that is fine don't change the database
            active_course.database.num_of_sections = active_course.database.num_of_sections
        try:  # modality
            if type(new_info.get("modality")) is not str or len(new_info.get("modality")) > 100:
                raise TypeError("modality expects a string")
            if new_info.get("modality") == '':
                raise KeyError  # Should go to except section because if string
                # is empty we don't replace the modality with nothing
            active_course.database.modality = new_info.get("modality")
        except KeyError:  # No name in list that is fine don't change the database
            active_course.database.modality = active_course.database.modality
        try:  # credits
            if type(new_info.get("credits")) is not int:
                raise TypeError("credits expects an int")
            active_course.database.credits = new_info.get("credits")
        except KeyError:  # No credits in list that is fine don't change the database
            active_course.database.credits = active_course.database.credits
        active_course.database.save()

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
        return self.database.user.email_address

    def getPassword(self):
        pass

    def getName(self):
        pass

    def getRole(self):
        return type(self.database)

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
        return self.database.user.email_address

    def getPassword(self):
        pass

    def getName(self):
        pass

    def getRole(self):
        return type(self.database)

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
        pass

    def getLabTAAsgmt(self):
        pass

    def addTA(self, active_ta):
        pass

    def removeTA(self):
        pass
