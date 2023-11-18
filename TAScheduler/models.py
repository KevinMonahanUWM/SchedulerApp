from django.db import models


class User(models.Model):
    email_address = models.CharField(max_length=90)  # This is also the username
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    home_address = models.CharField(max_length=90)
    phone_number = models.IntegerField()


class Course(models.Model):
    course_id = models.IntegerField()
    semester = models.CharField(max_length=11)


class Section(models.Model):
    section_id = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=30)
    meeting_time = models.DateTimeField()
    credits = models.IntegerField()


# noinspection DuplicatedCode
class TA(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sections = models.ManyToManyField(Section)


# noinspection DuplicatedCode
class TAToSection(models.Model):
    ta = models.ForeignKey(TA, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)


# noinspection DuplicatedCode
class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sections = models.ManyToManyField(Section)


# noinspection DuplicatedCode
class InstructorToSection(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)


class Administrator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
