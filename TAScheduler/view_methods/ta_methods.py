import abc
from dateutil import parser  # KEEP THIS

from TAScheduler.models import User, TA, Course, Lecture, Section, Lab, TAToCourse
from TAScheduler.view_methods.course_methods import CourseObj
from TAScheduler.view_methods.lab_methods import LabObj
from TAScheduler.view_methods.lecture_methods import LectureObj
from TAScheduler.view_methods.user_methods import UserObj


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
        return actualAsgmts >= maxAsgmts  # shouldn't ever be ">" but technically true if so (def can't be false)

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
        # Ensure that the TA is linked to the course of the lecture
        if not isinstance(active_lecture, LectureObj):
            raise TypeError("Sent in incorrect lecture type into the AssignTALec.")
        if not self.database.grader_status:
            raise RuntimeError("Can't assign TA a lec without grader status")

        if not TAToCourse.objects.filter(ta=self.database, course=active_lecture.getParentCourse()).exists():
            raise ValueError("TA is not assigned to the course of the lecture")

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

    def getAllUserAssignments(self):
        # Assuming 'CourseAsgmt' and 'SecAsgmt' are the related names for assignments in Course and Section models
        course_assignments = Course.objects.filter(assigned_to=self.database).values('name', 'assignments')
        section_assignments = Section.objects.filter(assigned_to=self.database).values('name', 'assignments')

        # Format assignments into the desired structure
        formatted_assignments = {
            "Role": self.get_role(),  # This method would need to be implemented to get the user's role
            "Username": self.getUsername(),
            "CourseAsgmts": list(course_assignments),
            "SecAsgmts": list(section_assignments),
        }
        return formatted_assignments

    def setSkills(self, skills):
        if (skills != "" and isinstance(skills, str)):
            self.database.skills = skills
            self.database.save()
        else:
            raise TypeError("Invalid skills input")