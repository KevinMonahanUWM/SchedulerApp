from dateutil import parser  # KEEP THIS

from TAScheduler.models import Administrator, User, TA, Instructor, Course, Lecture, Section, Lab, InstructorToCourse, \
    TAToCourse
from TAScheduler.view_methods.course_methods import CourseObj
from TAScheduler.view_methods.instructor_methods import InstructorObj
from TAScheduler.view_methods.lab_methods import LabObj
from TAScheduler.view_methods.lecture_methods import LectureObj
from TAScheduler.view_methods.section_methods import SectionObj
from TAScheduler.view_methods.ta_methods import TAObj
from TAScheduler.view_methods.user_methods import UserObj


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
            if len(str(user_info.get("phone_number"))) != 10:
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
        if not Course.objects.filter(course_id=section_info.get("course").course_id).exists():
            raise RuntimeError("Course ID is not existing course cant create section")

        courseDB = Course.objects.get(course_id=section_info.get("course").course_id)
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
                raise ValueError("location expects a str with a max length of 30")
            if new_info.get("location") == '':
                raise KeyError("missing field")
            active_section.database.section.location = new_info.get("location")
        except KeyError:  # Something
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
            if (User.objects.filter(email_address=new_info.get("email_address")).exists() and
                    active_user.database.user.email_address != new_info.get("email_address")):
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
            if new_info.get("phone_number") is None or new_info.get("phone_number") == 0:
                raise KeyError
            if len(new_info.get("phone_number")) != 10:
                raise ValueError("phone_number expects an int input with a length of 10")
            active_user.database.user.phone_number = int(new_info.get("phone_number"))
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
        elif not User.objects.filter(email_address=active_ta.getUsername()).exists():
            raise RuntimeError("User does not exist")
        if type(active_course) is not CourseObj:
            raise TypeError("Input passed is not a Course object")
        elif not Course.objects.filter(course_id=active_course.database.course_id).exists():
            raise RuntimeError("Course does not exist")
        if active_ta.getTACrseAsgmts().count() == active_ta.database.max_assignments:
            raise RuntimeError("Instructor is already assigned to max number of course permitted")
        TAToCourse.objects.create(ta=active_ta.database, course=active_course.database)

    def sectionTAAsmgt(self, active_ta, active_section):
        if not isinstance(active_ta, TA):
            raise TypeError("Input passed to admin.sectionTAAsmgt is not TA")
        if not isinstance(active_section, LabObj) and not isinstance(active_section, LectureObj):
            raise TypeError("Input passed to admin.sectionTAAsmgt is not Lab or Lecture")
        active_section.addTA(active_ta)

    def getAllCrseAsgmts(self):
        outputdict = {}
        if InstructorToCourse.objects.all().count() + TAToCourse.objects.all().count() == 0:
            raise RuntimeError("No course links exist")
        for i in InstructorToCourse.objects.all():
            outputdict[i.course.course_id] = i.instructor.user.email_address
        for i in TAToCourse.objects.all():
            if i.course.course_id in outputdict:
                outputdict[i.course.course_id] = (outputdict[i.course.course_id], i.ta.user.email_address)
            else:
                outputdict[i.course.course_id] = i.ta
        return outputdict

    def courseUserAsgmt(self, active_user, active_course):
        if not isinstance(active_course, CourseObj):
            raise TypeError("Input passed to admin.courseUserAsgmt is not CourseObj")
        if isinstance(active_user, InstructorObj):
            InstructorToCourse.objects.create(instructor=active_user.database, course=active_course.database)
        if isinstance(active_user, TAObj):
            TAToCourse.objects.create(ta=active_user.database, course=active_course.database)
        # Do .get method for a taToCourse or instructorToCourse
        if not isinstance(active_user, InstructorObj) and not isinstance(active_user, TAObj):
            raise TypeError("Input passed to admin.courseUserAsgmt is not InstructorObj or TAObj")

    def editContactInfo(self, **kwargs):
        user = self.database.user  # Accessing the User object

        # Validate each provided field
        for key, value in kwargs.items():
            if hasattr(user, key):
                if key == "email_address":
                    if not value or User.objects.filter(email_address=value).exists():
                        raise RuntimeError("Invalid or duplicate email address provided")
                elif key == "password":
                    if not value:
                        raise RuntimeError("Password not provided")
                elif key in ["first_name", "last_name", "home_address"]:
                    if not value:
                        raise RuntimeError(f"{key.replace('_', ' ').title()} not provided")
                elif key == "phone_number":
                    if not value or len(str(value)) != 10:
                        raise ValueError("Invalid phone number provided")
                else:
                    continue  # Skip if the key is not a valid field

                setattr(user, key, value)

        user.save()

    def getContactInfo(self):
        user = self.database.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email_address': user.email_address,
            'home_address': user.home_address,
            'phone_number': user.phone_number
        }

    def getAllSecAsgmt(self):
        qs = Section.objects.all()  # returns empty qs if no sections
        if qs.count() > 0:
            return qs
        else:
            raise RuntimeError("No active sections to return")