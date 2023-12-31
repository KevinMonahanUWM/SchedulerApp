from TAScheduler.models import User, Instructor, Course, Lecture, Section, InstructorToCourse
from TAScheduler.view_methods.user_methods import UserObj


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


    def getInstrCrseAsgmts(self):
        return InstructorToCourse.objects.filter(instructor=self.database)

    def getInstrLecAsgmts(self):  # new
        return Lecture.objects.filter(instructor=self.database)

    def editContactInfo(self, **kwargs):
        user = self.database.user  # Accessing the User object

        # Validate each provided field
        for key, value in kwargs.items():
            if hasattr(user, key):
                if key == "email_address":
                    # Basic email validation
                    if '@' not in value or '.' not in value:
                        raise RuntimeError("Invalid email address provided")
                    at_index = value.index('@')
                    dot_index = value.rindex('.')
                    # Ensuring '@' comes before the last '.'
                    if at_index >= dot_index or at_index == 0 or dot_index == len(value) - 1:
                        raise RuntimeError("Invalid email address provided")
                    if User.objects.filter(email_address=value).exists():
                        raise RuntimeError("Duplicate email address provided")
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
        course_assignments = Course.objects.filter(assigned_to=self.database).values('name', 'assignments')
        section_assignments = Section.objects.filter(assigned_to=self.database).values('name', 'assignments')

        # Format assignments into the desired structure
        formatted_assignments = {
            "Role": self.get_role(),
            "Username": self.getUsername(),
            "CourseAsgmts": list(course_assignments),
            "SecAsgmts": list(section_assignments),
        }
        return formatted_assignments