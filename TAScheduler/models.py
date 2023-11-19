from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(models.Model):
    email_address = models.CharField(max_length=90)  # This is also the username
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    home_address = models.CharField(max_length=90)
    phone_number = models.IntegerField()


# noinspection DuplicatedCode
class TA(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grader_status = models.BooleanField()
    max_assignments = models.IntegerField(
        default=6,
        validators=[
            MaxValueValidator(6),
            MinValueValidator(0)
        ]
    )


class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    max_assignments = models.IntegerField(
        default=6,
        validators=[
            MaxValueValidator(6),
            MinValueValidator(0)
        ]
    )


class Course(models.Model):
    course_id = models.IntegerField()
    semester = models.CharField(max_length=11)


class Section(models.Model):
    section_id = models.IntegerField()
    ta = models.ForeignKey(TA, unique=True, on_delete=models.SET_NULL, null=True)
    instructor = models.ForeignKey(Instructor, unique=True, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=30)
    meeting_time = models.DateTimeField()
    credits = models.IntegerField()


# noinspection DuplicatedCode
class TAToCourse(models.Model):
    ta = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)


class InstructorToCourse(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)


class Administrator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
