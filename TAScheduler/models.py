from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(models.Model):
    email_address = models.CharField(max_length=90)  # This is also the username
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    home_address = models.CharField(max_length=90)
    phone_number = models.IntegerField()

    def __str__(self):
        return self.first_name + " " + self.last_name + ": " + self.email_address


# noinspection DuplicatedCode
class TA(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    grader_status = models.BooleanField()
    skills = models.TextField(null=True, default="No skills listed")
    max_assignments = models.IntegerField(
        default=6,
        validators=[
            MaxValueValidator(6),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return self.user.__str__() + " -  TA"


class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    max_assignments = models.IntegerField(
        default=6,
        validators=[
            MaxValueValidator(6),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return self.user.__str__() + " -  Instructor"


class Course(models.Model):
    course_id = models.IntegerField()
    semester = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    num_of_sections = models.IntegerField()
    modality = models.CharField(max_length=100)

    def __str__(self):
        return str(self.course_id) + ": " + self.name


class Section(models.Model):
    section_id = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    location = models.CharField(max_length=30)
    meeting_time = models.DateTimeField()

    def __str__(self):  # for "determineSection"
        return str(self.section_id) + "- " + str(self.course)


class Lab(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=False)
    ta = models.ForeignKey(TA, unique=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):  # for "determineSection"
        return "Lab:" + self.section.__str__()

    def toDict(self):  # for display
        return {"section_type": "Lab", "section_id": self.section.section_id,
                "course_id": self.section.course.course_id}


class Lecture(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=False)
    instructor = models.ForeignKey(Instructor, unique=True, on_delete=models.SET_NULL, null=True)
    ta = models.ForeignKey(TA, unique=True, on_delete=models.SET_NULL,
                           null=True)  # Graders would be assigned to lecture

    def __str__(self):  # for "determineSection"
        return "Lecture:" + self.section.__str__()

    def toDict(self):  # for display
        return {"section_type": "Lecture", "section_id": self.section.section_id,
                "course_id": self.section.course.course_id}


class TAToCourse(models.Model):
    ta = models.ForeignKey(TA, on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)


class InstructorToCourse(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)


class Administrator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.user.__str__() + " -  Administrator"
