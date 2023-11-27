import abc

from dateutil import parser

from TAScheduler.models import Administrator, User, TA, Instructor, Course, Lecture, Section, Lab, InstructorToCourse, \
    TAToCourse


class UserObj(abc.ABC):

    def __init__(self):
        self.database = None

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
        super().__init__()
        if type(admin_info) is not Administrator:
            raise TypeError("Data passed to init method is not a member of the Administrator database class")
        elif not User.objects.filter(email_address=admin_info.user.email_address).exists():
            raise TypeError("The administrator object does not exist in the database")
        self.database = admin_info

    def getUsername(self):
        return self.database.user.email_address

    def getPassword(self):
        return self.database.user.password

    def getName(self):
        return self.database.user.first_name + " " + self.database.user.last_name

    def getRole(self):
        return str(type(self.database))

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
            raise TypeError("Input passed is not a subclass of user obj")
        elif not User.objects.filter(email_address=active_user.getUsername()).exists():
            raise RuntimeError("User does not exist")
        User.delete(active_user.database.user)

    def removeSection(self, active_section):
        if not isinstance(active_section, SectionObj):
            raise TypeError("Input passed is not a subclass of section obj")
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
            if new_info.get("course_id") is None:
                raise KeyError
            if type(new_info.get("course_id")) is not int or new_info.get("course_id") < 0:
                raise ValueError("Course id expects an int")
            if Course.objects.filter(course_id=new_info.get("course_id")).exists():
                raise RuntimeError("Can not have two courses with the same course number")
            active_course.database.course_id = new_info.get("course_id")
        except KeyError:  # No course_id in list that is fine don't change the database
            active_course.database.course_id = active_course.database.course_id
        try:  # Semester
            if new_info.get("semester") is None:
                raise KeyError
            if type(new_info.get("semester")) is not str or len(new_info.get("semester")) > 11:
                raise ValueError("semester expects a string")
            if new_info.get("name") == '':
                raise KeyError  # Should go to except section because if string
                # is empty we don't replace the name with nothing
            active_course.database.semester = new_info.get("semester")
        except KeyError:  # No semester in list that is fine don't change the database
            active_course.database.semester = active_course.database.semester
        try:  # Name
            if new_info.get("name") is None:
                raise KeyError
            if type(new_info.get("name")) is not str or len(new_info.get("name")) > 100:
                raise ValueError("name expects a string")
            if new_info.get("name") == '':
                raise KeyError  # Should go to except section because if string
                # is empty we don't replace the name with nothing
            active_course.database.name = new_info.get("name")
        except KeyError:  # No name in list that is fine don't change the database
            active_course.database.name = active_course.database.name
        try:  # Description
            if new_info.get("description") is None:
                raise KeyError
            if type(new_info.get("description")) is not str or len(new_info.get("description")) > 1000:
                raise ValueError("description expects a string")
            if new_info.get("description") == '':
                raise KeyError  # Should go to except section because if string
                # is empty we don't replace the description with nothing
            active_course.database.description = new_info.get("description")
        except KeyError:  # No description in list that is fine don't change the database
            active_course.database.description = active_course.database.description
        try:  # num_of_sections
            if new_info.get("num_of_sections") is None:
                raise KeyError
            if type(new_info.get("num_of_sections")) is not int or new_info.get("num_of_sections") < 0:
                raise ValueError("num_of_sections expects an int")
            active_course.database.num_of_sections = new_info.get("num_of_sections")
        except KeyError:  # No num_of_sections in list that is fine don't change the database
            active_course.database.num_of_sections = active_course.database.num_of_sections
        try:  # modality
            if new_info.get("modality") is None:
                raise KeyError
            if type(new_info.get("modality")) is not str or len(new_info.get("modality")) > 100:
                raise ValueError("modality expects a string")
            if new_info.get("modality") == '':
                raise KeyError  # Should go to except section because if string
                # is empty we don't replace the modality with nothing
            active_course.database.modality = new_info.get("modality")
        except KeyError:  # No name in list that is fine don't change the database
            active_course.database.modality = active_course.database.modality
        try:  # credits
            if new_info.get("credits") is None:
                raise KeyError
            if type(new_info.get("credits")) is not int or new_info.get("credits") < 0:
                raise ValueError("credits expects an int")
            active_course.database.credits = new_info.get("credits")
        except KeyError:  # No credits in list that is fine don't change the database
            active_course.database.credits = active_course.database.credits
        active_course.database.save()

    def editSection(self, active_section, new_info):  # new inputs
        if not isinstance(active_section, SectionObj):
            raise TypeError("Input passed is not a subclass of section obj")
        elif not Section.objects.filter(section_id=active_section.getID()).exists():
            raise RuntimeError("Section does not exist")
        if type(new_info) is not dict:
            raise TypeError("Input passed is not a dictionary")

        try:  # section_id
            if new_info.get("section_id") is None:
                raise KeyError
            if type(new_info.get("section_id")) is not int or new_info.get("section_id") < 0:
                raise ValueError("section_id expects an int")
            if Section.objects.filter(section_id=new_info.get("section_id")).exists():
                raise RuntimeError("Can not have two sections with the same section number")
            active_section.database.section.section_id = new_info.get("section_id")
        except KeyError:  # No course_id in list that is fine don't change the database
            active_section.database.section.section_id = active_section.database.section.section_id
        try:  # location
            if new_info.get("location") is None:
                raise KeyError
            if type(new_info.get("location")) is not str or len(new_info.get("location")) > 30:
                raise ValueError("location expects a str")
            if new_info.get("location") == '':
                raise KeyError
            active_section.database.section.location = new_info.get("location")
        except KeyError:
            active_section.database.section.location = active_section.database.section.location
        try:  # meeting_time
            if new_info.get("meeting_time") is None:
                raise KeyError
            parsed_date = parser.parse(new_info.get("meeting_time"))
            parsed_date.strftime("%Y-%m-%d %H:%M:%S")  # Will throw ValueError if datetime is wrong format
            if new_info.get("meeting_time") == '':
                raise KeyError
            active_section.database.section.meeting_time = new_info.get("meeting_time")
        except KeyError:
            active_section.database.section.meeting_time = active_section.database.section.meeting_time
        active_section.database.section.save()

    def editUser(self, active_user, new_info):  # new inputs
        if not isinstance(active_user, UserObj):
            raise TypeError("Input passed is not a subclass of user obj")
        elif not User.objects.filter(email_address=active_user.getUsername()).exists():
            raise RuntimeError("User does not exist")
        if type(new_info) is not dict:
            raise TypeError("Input passed is not a dictionary")

        try:  # email_address
            if new_info.get("email_address") is None:
                raise KeyError
            if type(new_info.get("email_address")) is not str or len(new_info.get("email_address")) > 90:
                raise ValueError("Email address excepts input of a str")
            if User.objects.filter(email_address=new_info.get("email_address")).exists():
                raise RuntimeError("Can not have multiple users with the same email address")
            if new_info.get("email_address") == "":
                raise KeyError
            active_user.database.user.email_address = new_info.get("email_address")
        except KeyError:  # No email address in list that is fine don't change the database
            active_user.database.user.email_address = active_user.database.user.email_address
        try:  # password
            if new_info.get("password") is None:
                raise KeyError
            if type(new_info.get("password")) is not str or len(new_info.get("password")) > 30:
                raise ValueError("password excepts input of a str")
            if new_info.get("password") == "":
                raise KeyError
            active_user.database.user.password = new_info.get("password")
        except KeyError:  # No password in list that is fine don't change the database
            active_user.database.user.password = active_user.database.user.password
        try:  # first_name
            if new_info.get("first_name") is None:
                raise KeyError
            if type(new_info.get("first_name")) is not str or len(new_info.get("first_name")) > 30:
                raise ValueError("first_name excepts input of a str")
            if new_info.get("first_name") == "":
                raise KeyError
            active_user.database.user.first_name = new_info.get("first_name")
        except KeyError:  # No first_name in list that is fine don't change the database
            active_user.database.user.first_name = active_user.database.user.first_name
        try:  # last_name
            if new_info.get("last_name") is None:
                raise KeyError
            if type(new_info.get("last_name")) is not str or len(new_info.get("last_name")) > 30:
                raise ValueError("last_name excepts input of a str")
            if new_info.get("last_name") == "":
                raise KeyError
            active_user.database.user.last_name = new_info.get("last_name")
        except KeyError:  # No last name in list that is fine don't change the database
            active_user.database.user.last_name = active_user.database.user.last_name
        try:  # home_address
            if new_info.get("home_address") is None:
                raise KeyError
            if type(new_info.get("home_address")) is not str or len(new_info.get("home_address")) > 90:
                raise ValueError("home_address excepts input of a str")
            if new_info.get("home_address") == "":
                raise KeyError
            active_user.database.user.home_address = new_info.get("home_address")
        except KeyError:  # No home_address in list that is fine don't change the database
            active_user.database.user.home_address = active_user.database.user.home_address
        try:  # phone number
            if new_info.get("phone_number") is None:
                raise KeyError
            if type(new_info.get("phone_number")) is not int or len(str(new_info.get("phone_number"))) is not 10:
                raise ValueError("phone_number expects an int input with a length of 10")
            active_user.database.user.phone_number = new_info.get("phone_number")
        except KeyError:
            active_user.database.user.phone_number = active_user.database.user.phone_number
        active_user.database.user.save()
        role = active_user.getRole()
        if role == "<class 'TAScheduler.models.TA'>":
            try:  # grader_status
                if new_info.get("grader_status") is None:
                    raise KeyError
                if type(new_info.get("grader_status")) is not bool:
                    raise ValueError("grader_status expects boolean as input")
                active_user.database.grader_status = new_info.get("grader_status")
            except KeyError:  # no grader status in dict
                active_user.database.grader_status = active_user.database.grader_status
            try:  # max assignments
                if new_info.get("max_assignments") is None:
                    raise KeyError
                if type(new_info.get("max_assignments")) is not int or (
                        new_info.get("max_assignments") < 0 or new_info.get("max_assignments") > 6):
                    raise ValueError("max_assignments expects an int as input between 0 and 6")
                active_user.database.max_assignments = new_info.get("max_assignments")
            except KeyError:
                active_user.database.max_assignments = active_user.database.max_assignments
        elif role == "<class 'TAScheduler.models.Instructor'>":
            try:  # max assignments
                if new_info.get("max_assignments") is None:
                    raise KeyError
                if type(new_info.get("max_assignments")) is not int or (
                        new_info.get("max_assignments") < 0 or new_info.get("max_assignments") > 6):
                    raise ValueError("max_assignments expects an int as input between 0 and 6")
                active_user.database.max_assignments = new_info.get("max_assignments")
            except KeyError:
                active_user.database.max_assignments = active_user.database.max_assignments
        active_user.database.save()

    def courseInstrAsmgt(self, active_instr, active_course):  # new inputs
        if not isinstance(active_instr, InstructorObj):
            raise TypeError("Input passed is not an object of instructor obj")
        elif not User.objects.filter(email_address=active_instr.getUsername()).exists():
            raise RuntimeError("User does not exist")
        if type(active_course) is not CourseObj:
            raise TypeError("Input passed is not a Course object")
        elif not Course.objects.filter(course_id=active_course.database.course_id).exists():
            raise RuntimeError("Course does not exist")
        if active_instr.getInstrCrseAsgmts().count() == active_instr.database.max_assignments:
            raise RuntimeError("Instructor is already assigned to max number of course permitted")
        InstructorToCourse.objects.create(instructor=active_instr.database, course=active_course.database)

    def courseTAAsmgt(self, active_ta, active_course):  # new remove sectionTAAsmgt
        if not isinstance(active_ta, TAObj):
            raise TypeError("Input passed is not an object of ta obj")
        elif not User.objects.filter(email_address=active_ta.getUsername()).exists():
            raise RuntimeError("User does not exist")
        if type(active_course) is not CourseObj:
            raise TypeError("Input passed is not a Course object")
        elif not Course.objects.filter(course_id=active_course.database.course_id).exists():
            raise RuntimeError("Course does not exist")
        if active_ta.getTACrseAsgmts().count() == active_ta.database.max_assignments:
            raise RuntimeError("Instructor is already assigned to max number of course permitted")
        TAToCourse.objects.create(ta=active_ta.database, course=active_course.database)


class TAObj(UserObj):
    database = None

    def __init__(self, ta_info):
        super().__init__()
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
        return self.database.user.password

    def getName(self):
        return self.database.user.first_name + " " + self.database.user.last_name

    def getRole(self):
        return str(type(self.database))

    def hasMaxAsgmts(self):
        pass

    def assignTACourse(self, active_course):
        pass

    def assignTALab(self, active_lab):
        pass

    def assignTALecture(self, active_lecture):  # new
        pass

    def getTACrseAsgmts(self):
        return TAToCourse.objects.filter(ta=self.database)

    def getTALabAsgmts(self):
        pass

    def getTALecAsgmts(self):  # new
        pass

    def getGraderStatus(self):
        pass


class InstructorObj(UserObj):
    database = None

    def __init__(self, instr_info):
        super().__init__()
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
        return self.database.user.password

    def getName(self):
        return self.database.user.first_name + " " + self.database.user.last_name

    def getRole(self):
        return str(type(self.database))

    def hasMaxAsgmts(self):
        pass

    def assignInstrCourse(self, active_course):
        pass

    def assignInstrLecture(self, active_lecture):  # new.
        pass

    def getInstrCrseAsgmts(self):
        return InstructorToCourse.objects.filter(instructor=self.database)

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

    def __init__(self):
        self.database = None

    @abc.abstractmethod
    def getID(self):
        pass

    @abc.abstractmethod
    def getParentCourse(self):
        pass


class LectureObj(SectionObj):
    database = None

    def __init__(self, lecture_info):
        super().__init__()
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
        super().__init__()
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
