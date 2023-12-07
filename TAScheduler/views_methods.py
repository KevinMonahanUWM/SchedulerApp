import abc
from dateutil import parser  # KEEP THIS

from TAScheduler.models import Administrator, User, TA, Instructor, Course, Lecture, Section, Lab, InstructorToCourse, \
    TAToCourse


class UserObj(abc.ABC):

    def __init__(self):
        self.database = None

    @abc.abstractmethod
    def login(self, email_address, password):
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
        return "Admin"

    def login(self, username, password):
        try:
            User.objects.get(email_address=username, password=password)  # Correct field name\
            return True
        except User.DoesNotExist:
            return False  # display "Invalid username or password."

    def createCourse(self, course_info):
        if Course.objects.filter(course_id=course_info.get('course_id')).exists():
            raise RuntimeError("Course with this ID already exists")
        new_course = Course.objects.create(**course_info)
        return new_course

    def createUser(self, user_info, role):
        if type(user_info) is not dict:
            raise TypeError("Input passed is not a dictionary")
        if User.objects.filter(email_address=user_info.get('email_address')).exists():
            raise RuntimeError("User with this email address already exists")
        try:
            if user_info.get('email_address') == "":
                raise RuntimeError("Not all inputs have been provided")
        except KeyError:
            raise RuntimeError("Not all inputs have been provided")
        try:
            if user_info.get('password') == "":
                raise RuntimeError("Not all inputs have been provided")
        except KeyError:
            raise RuntimeError("Not all inputs have been provided")
        try:
            if user_info.get('first_name') == "":
                raise RuntimeError("Not all inputs have been provided")
        except KeyError:
            raise RuntimeError("Not all inputs have been provided")
        try:
            if user_info.get('last_name') == "":
                raise RuntimeError("Not all inputs have been provided")
        except KeyError:
            raise RuntimeError("Not all inputs have been provided")
        try:
            if user_info.get('home_address') == "":
                raise RuntimeError("Not all inputs have been provided")
        except KeyError:
            raise RuntimeError("Not all inputs have been provided")
        try:
            if user_info.get('phone_number') == 0:
                raise RuntimeError("Not all inputs have been provided")
            if len(str(user_info.get("phone_number"))) is not 10:
                raise ValueError("phone_number expects an int input with a length of 10")
        except KeyError:
            raise RuntimeError("Not all inputs have been provided")
        if role == "" or role is None:
            raise RuntimeError("Not all inputs have been provided")
        new_user = User.objects.create(
            email_address=user_info.get('email_address'),
            password=user_info.get('password'),
            first_name=user_info.get('first_name'),
            last_name=user_info.get('last_name'),
            home_address=user_info.get('home_address'),
            phone_number=user_info.get('phone_number')
        )
        if role.lower() == 'admin':
            Administrator.objects.create(user=new_user)
        elif role.lower() == 'ta':
            TA.objects.create(user=new_user, grader_status=False)
        elif role.lower() == 'instructor':
            Instructor.objects.create(user=new_user)
        return new_user

    def createSection(self, section_info):
        if any(value == "" for value in section_info.values()):
            raise RuntimeError("No missing section fields allowed")
        if Section.objects.filter(section_id=section_info.get('section_id')).exists():
            raise RuntimeError("Section with this ID already exists")
        if not Course.objects.filter(course_id=section_info.get('course').course_id).exists():
            raise RuntimeError("Course ID is not existing course cant create section")

        courseDB = Course.objects.get(course_id=section_info.get('course').course_id)
        fields = {"section_id": section_info["section_id"],
                  "course": courseDB,
                  "location": section_info["location"],
                  "meeting_time": section_info["meeting_time"]}
        new_section = Section.objects.create(**fields)

        if (section_info["section_type"] == "Lab"):
            new_section = Lab.objects.create(section=new_section)
        else:
            new_section = Lecture.objects.create(section=new_section)
        return new_section

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
        print(isinstance(active_section, LectureObj))
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
            raise TypeError("Input passed is not a subclass of sectionobj")
        elif not Section.objects.filter(section_id=active_section.getID()).exists():
            raise RuntimeError("Section does not exist")
        if type(new_info) is not dict:
            raise TypeError("Input passed is not a dictionary")

        try:  # section_id
            if new_info.get("section_id") is None:
                raise KeyError("missing field")
            if type(new_info.get("section_id")) is not int or new_info.get("section_id") < 0:
                raise ValueError("section_id expects an int")
            if Section.objects.filter(section_id=new_info.get("section_id")).exists() and (
                    new_info.get("section_id") != active_section.database.section.section_id):
                raise RuntimeError("Can not have two sections with the same section number")
            active_section.database.section.section_id = new_info.get("section_id")
        except KeyError:  # No course_id in list that is fine don't change the database
            active_section.database.section.section_id = active_section.database.section.section_id
        try:  # location
            if new_info.get("location") is None:
                raise KeyError("missing field")
            if type(new_info.get("location")) is not str or len(new_info.get("location")) > 30:
                raise ValueError("location expects a str")
            if new_info.get("location") == '':
                raise KeyError("missing field")
            active_section.database.section.location = new_info.get("location")
        except KeyError:
            active_section.database.section.location = active_section.database.section.location
        try:  # meeting_time
            if new_info.get("meeting_time") is None:
                raise KeyError("missing field")
            parsed_date = parser.parse(new_info.get("meeting_time"))
            temp = parsed_date.strftime("%Y-%m-%d %H:%M:%S")  # Will throw ValueError if datetime is wrong format
            if new_info.get("meeting_time") == '':
                raise KeyError("missing field")
            active_section.database.section.meeting_time = new_info.get("meeting_time")
        except KeyError:
            active_section.database.section.meeting_time = active_section.database.section.meeting_time
        active_section.database.section.save()

    def editUser(self, active_user, new_info):  # new inputs
        if not isinstance(active_user, UserObj):
            raise TypeError("Input passed is not a subclass of userobj")
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
            if new_info.get("phone_number") is None or new_info.get("phone_number") is 0:
                raise KeyError
            if type(new_info.get("phone_number")) is not int or len(str(new_info.get("phone_number"))) is not 10:
                raise ValueError("phone_number expects an int input with a length of 10")
            active_user.database.user.phone_number = new_info.get("phone_number")
        except KeyError:
            active_user.database.user.phone_number = active_user.database.user.phone_number
        active_user.database.user.save()
        role = active_user.getRole()
        if role == "TA":
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
        elif role == "Instructor":
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
        elif not User.objects.filter(email_address=active_ta.getUsername()).exists():  # I believe this is a redundant
            # test as a TAObj cannot be made without a username
            raise RuntimeError("User does not exist")
        if type(active_course) is not CourseObj:
            raise TypeError("Input passed is not a Course object")
        elif not Course.objects.filter(course_id=active_course.database.course_id).exists():
            raise RuntimeError("Course does not exist")
        if active_ta.getTACrseAsgmts().count() == active_ta.database.max_assignments:
            raise RuntimeError("Instructor is already assigned to max number of course permitted")
        TAToCourse.objects.create(ta=active_ta.database, course=active_course.database)

    def sectionTAAsmgt(self, active_ta, active_course):
        pass

    def getAllCrseAsgmts(self):
        pass

    def courseUserAsgmt(self, active_user, active_course):
        # Do .get method for a taToCourse or instructorToCourse
        pass


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
        try:
            User.objects.get(email_address=username, password=password)  # Correct field name\
            return True
        except User.DoesNotExist:
            return False  # display "Invalid username or password."

    def getUsername(self):
        return self.database.user.email_address

    def getPassword(self):
        return self.database.user.password

    def getName(self):
        return self.database.user.first_name + " " + self.database.user.last_name

    def getRole(self):
        return "TA"

    def hasMaxAsgmts(self):
        maxAsgmts = self.database.max_assignments
        actualAsgmts = TAToCourse.objects.filter(ta=self.database).count()
        return (actualAsgmts >= maxAsgmts)  # shouldn't ever be ">" but technically true if so (def can't be false)

    def assignTACourse(self, active_course):  # ADJUSTED TESTS!
        if not isinstance(active_course, CourseObj):
            raise TypeError("Sent in incorrect course type into the AssignTACourse.")
        courseDB = active_course.database
        if not Course.objects.filter(course_id=courseDB.course_id).exists():
            raise ValueError("The provided Course object does not have an equivalent record in the database.")
        if TAToCourse.objects.filter(ta=self.database, course=courseDB).exists():
            raise ValueError("Can't assign a course already assigned to this TA.")
        if courseDB.num_of_sections == TAToCourse.objects.filter(course=courseDB).count():
            raise ValueError("Can't assign course that has reached it's maximum assignments")
        if self.hasMaxAsgmts():  # not sure what error this is
            raise ValueError("Can't assign a course past a TA's maximum capacity")

        TAToCourse(course=courseDB, ta=self.database).save()  # Assign the course? Is that it?

    #
    def assignTALab(self, active_lab):
        if not isinstance(active_lab, LabObj):
            raise TypeError("Sent in incorrect lab type into the AssignTALab.")
        if self.database.grader_status:
            raise RuntimeError("Can't assign TA a lab with grader status")

        argLabDB = active_lab.database
        if argLabDB.section is None:  # SHOULD BE IMPOSSIBLE*
            raise ValueError("The provided Lab object does not have an equivalent section record in the database.")
        if not argLabDB.ta is None:
            raise ValueError("Can't assign a lab that already have a TA.")

        secDB = argLabDB.section
        qs = Lab.objects.filter(section=secDB, ta=self.database)
        if qs.count() > 0:
            raise ValueError("Can't assign a lab already assigned to this TA.")

        argLabDB.ta = self.database
        argLabDB.save()  # Assign the lab? Is that it?

    def assignTALecture(self, active_lecture):  # new
        if not isinstance(active_lecture, LectureObj):
            raise TypeError("Sent in incorrect lecture type into the AssignTALec.")
        if not self.database.grader_status:
            raise RuntimeError("Can't assign TA a lec without grader status")

        argLecDB = active_lecture.database
        if argLecDB.section is None:  # SHOULD BE IMPOSSIBLE*
            raise ValueError("The provided Lab object does not have an equivalent section record in the database.")
        if not argLecDB.ta is None:
            raise ValueError("Can't assign a lec that already have a TA.")

        argSecDB = argLecDB.section
        qs = Lecture.objects.filter(section=argSecDB, ta=self.database)
        if qs.count() > 0:
            raise ValueError("Can't assign a lecture already assigned to this TA.")

        argLecDB.ta = self.database
        argLecDB.save()  # Assign the lec? Is that it?

    def getTACrseAsgmts(self):
        return TAToCourse.objects.filter(ta=self.database)

    def getTALabAsgmts(self):
        return Lab.objects.filter(ta=self.database)

    def getTALecAsgmts(self):  # new
        return Lecture.objects.filter(ta=self.database)

    def getGraderStatus(self):
        return self.database.grader_status


class InstructorObj(UserObj):
    database = None

    def __init__(self, info):
        super().__init__()
        if type(info) is not Instructor:
            raise TypeError("Data passed to init method is not a member of the Instructor database class")
        elif not User.objects.filter(email_address=info.user.email_address).exists():
            raise TypeError("The instructor object does not exist in the database")
        self.database = info

    def login(self, username, password):
        try:
            User.objects.get(email_address=username, password=password)  # Correct field name\
            return True
        except User.DoesNotExist:
            return False  # display "Invalid username or password."

    def getUsername(self):
        return self.database.user.email_address

    def getPassword(self):
        return self.database.user.password

    def getName(self):
        return self.database.user.first_name + " " + self.database.user.last_name

    def getRole(self):
        return "Instructor"

    def hasMaxAsgmts(self):
        maxAsgmts = self.database.max_assignments
        actualAsgmts = InstructorToCourse.objects.filter(instructor=self.database).count()
        return (actualAsgmts >= maxAsgmts)  # shouldn't ever be ">" but technically true if so (def can't be false)

    def assignInstrCourse(self, active_course):
        if not isinstance(active_course, CourseObj):
            raise TypeError("Sent in incorrect course type into the AssignInstrCourse.")
        courseDB = active_course.database
        if not Course.objects.filter(course_id=courseDB.course_id).exists():
            raise ValueError("The provided Course object does not have an equivalent record in the database.")
        if InstructorToCourse.objects.filter(instructor=self.database, course=courseDB).exists():
            raise ValueError("Can't assign a course already assigned to this instructor.")
        if courseDB.num_of_sections == InstructorToCourse.objects.filter(course=courseDB).count():
            raise ValueError("Can't assign course that has reached it's maximum assignments")
        if self.hasMaxAsgmts():  # not sure what error this is
            raise ValueError("Can't assign a course past a instructor's maximum capacity")

        InstructorToCourse(course=courseDB, instructor=self.database).save()

    def assignInstrLecture(self, active_lecture):  # new
        if not isinstance(active_lecture, LectureObj):
            raise TypeError("Sent in incorrect lecture type into the AssignTALec.")

        argLecDB = active_lecture.database
        if argLecDB.section is None:  # SHOULD BE IMPOSSIBLE*
            raise ValueError("The provided Lab object does not have an equivalent section record in the database.")
        if not argLecDB.instructor is None:
            raise ValueError("Can't assign a lec that already have a instr.")

        argSecDB = argLecDB.section
        qs = Lecture.objects.filter(section=argSecDB, instructor=self.database)
        if qs.count() > 0:
            raise ValueError("Can't assign a lecture already assigned to this instructor.")

        argLecDB.instructor = self.database
        argLecDB.save()  # Assign the lec? Is that it?

    def getInstrCrseAsgmts(self):
        return InstructorToCourse.objects.filter(instructor=self.database)

    def getInstrLecAsgmts(self):  # new
        return Lecture.objects.filter(instructor=self.database)


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
            'modality': self.database.modality,
            'credits': self.database.credits
        }


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
        return self.database.section.course

    def getLectureTAAsgmt(self):  # new
        return self.database.ta

    def addTA(self, active_ta):  # new
        if type(active_ta) is not TA:
            raise TypeError("Data passed to addTA method is not a TA")
        elif not TA.objects.filter(user=active_ta.user).exists():
            raise RuntimeError("The TA object does not exist in the database")
        elif self.database.ta is not None:
            raise RuntimeError("A TA already exists in lecture")
        self.database.ta = active_ta

    def getLecInstrAsmgt(self):
        return self.database.instructor

    def addInstr(self, active_instr):
        if type(active_instr) is not Instructor:
            raise TypeError("Data passed to addInstructor method is not a Instructor")
        elif not Instructor.objects.filter(user=active_instr.user).exists():
            raise RuntimeError("The Instructor object does not exist in the database")
        elif self.database.instructor is not None:
            raise RuntimeError("An Instructor already exists in lecture")
        self.database.instructor = active_instr

    def removeInstr(self):
        if self.database.instructor is None:
            raise RuntimeError("No instructor to remove from lecture")
        self.database.instructor = None

    def removeTA(self):  # new
        if self.database.ta is None:
            raise RuntimeError("No TA to remove from lecture")
        self.database.ta = None


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
        return self.database.section.course

    def getLabTAAsgmt(self):
        return self.database.ta

    def addTA(self, active_ta):
        if type(active_ta) is not TA:
            raise TypeError("Data passed to addTA method is not a TA")
        elif not TA.objects.filter(user=active_ta.user).exists():
            raise RuntimeError("The TA object does not exist in the database")
        elif self.database.ta is not None:
            raise RuntimeError("A TA already exists in lab")
        self.database.ta = active_ta

    def removeTA(self):
        if self.database.ta is None:
            raise RuntimeError("No TA to remove from lab")
        self.database.ta = None
