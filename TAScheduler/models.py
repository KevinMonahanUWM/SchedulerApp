from django.db import models

class User(models.Model):
    email_address = models.Charfield(max_length=90) # This is also the username
    password = models.Charfield(max_length=30)
    first_name = models.Charfield(max_length=30)
    last_name = models.Charfield(max_length=30)
    home_address = models.Charfield(max_length=90)
    phone_number = models.IntegerField()

class TA(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sections = models.ManyToManyField(Section)

class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sections = models.ManyToManyField(Section)

class Administrator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Course(models.Model):
    course_id = models.IntegerField()
    semester = models.Charfield(max_length=11)


class Section(models.Model):
    section_id = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    location = models.Charfield(max_length=30)
    meeting_time = models.DateTimeField()
    credits = models.IntegerField()
