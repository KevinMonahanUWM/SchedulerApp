from datetime import datetime

from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

from TAScheduler.models import User, Administrator, Instructor, TA, Lecture, Section, Lab
from TAScheduler.views_methods import TAObj, InstructorObj, AdminObj, LabObj, LectureObj


# Mostly temporary to get basic skeleton working
# TODO add post methods and make login screen default
# TODO fix the get methods to pass content information
# TODO make each page require correct session token to access
def determineUser(user):  # Str generated by the database
    email = user.split(": ", 1)[1]
    email_role = email.split(" -  ", 1)
    selected_user = User.objects.get(email_address=email_role[0])
    if email_role[1].lower() == "ta":
        user_object = TAObj(TA.objects.get(user=selected_user))
    elif email_role[1].lower() == "instructor":
        user_object = InstructorObj(Instructor.objects.get(user=selected_user))
    else:
        user_object = AdminObj(Administrator.objects.get(user=selected_user))
    return user_object


def determineSec(section):  # Take "formatted str", return lab/lec obj.
    secInfo = section.split("- ", 1)  # Ex: (Lecture)[0] & (Section ID:#, Course ID:#)[1]
    secCrseInfo = secInfo[1].split(", ", 1)  # Ex: (Section ID:#)[0] & (Course ID:#)[1]
    secID = int(secCrseInfo[0].split(":")[1])  # Ex: (Section ID)[0] & (#)[1]
    try:
        secDB = Section.objects.get(section_id=secID)
        if secInfo[0] == "Lab":
            secObj = LabObj(Lab.objects.get(section=secDB))
        else:  # if not lab assuming it's a lecture
            secObj = LectureObj(Lecture.objects.get(section=secDB))
        return secObj
    except:
        raise RuntimeError("Section does not exist in Database")


class Login(View):

    def get(self, request):
        return render(request, "login.html")


class Home(View):

    def get(self, request):
        return render(request, "home.html")


class CourseManagement(View):

    def get(self, request):
        return render(request, "courseManagement/course_management.html")


class CreateCourse(View):

    def get(self, request):
        return render(request, "courseManagement/create_course.html")


class DeleteCourse(View):

    def get(self, request):
        return render(request, "courseManagement/delete_course.html")


class EditCourse(View):

    def get(self, request):
        return render(request, "courseManagement/edit_course.html")


class AddInstructorToCourse(View):

    def get(self, request):
        return render(request, "courseManagement/add_instructor_to_course.html")


class AccountManagement(View):

    def get(self, request):
        return render(request, "accountManagement/account_management.html")


class CreateAccount(View):

    def get(self, request):
        return render(request, "accountManagement/create_account.html")


class DeleteAccount(View):

    def get(self, request):
        return render(request, "accountManagement/delete_account.html")


class EditAccount(View):

    def get(self, request):
        return render(request, "accountManagement/edit_account.html")


class SectionManagement(View):

    def get(self, request):
        return render(request, "sectionManagement/section_management.html")


class CreateSection(View):
    def get(self, request):
        secs = ["Lab", "Lecture"]  # For dropdown
        return render(request, "sectionManagement/create_section.html", {"secs": secs})

    def post(self, request):
        curUserEmail = request.session["user"]  # should hold unique identifier "email"
        # Next sprint will require us to search for the user in the DB: current user may not be an admin
        curUserObj = AdminObj(Administrator(user=User.objects.get(email_address=curUserEmail)))

        course_id = request.POST.get('course_id')
        section_id = request.POST.get('section_id')
        section_type = request.POST.get('section_type')
        meeting_time = request.POST.get('meeting_time')
        location = request.POST.get('location')

        secInfo = {'course_id': course_id, 'section_id': section_id,
                   'section_type': section_type, 'meeting_time': meeting_time, 'location': location}
        try:
            curUserObj.createSection(secInfo)
            return render(request, "success.html", {"message": "Successfully Created Section",
                                                    "previous_url": "/home/managesection/create"})
        except Exception as e:  # THIS TAKES THE MESSAGE INSIDE OF THE EXCEPTION AND STORES AS e, ValueError("me") <- "me"
            return render(request, "error.html", {"message": e, "previous_url": "/home/managesection/create"})


class DeleteSection(View):

    def get(self, request):
        # Different that Kevin's approach (it's for displaying:"Lecture- Section ID:#, Course ID:#")
        sections = list()
        for lecture in Lecture.objects.all():
            d = lecture.toDict()
            sections.append(
                d["section_type"] + "- Section ID:" + str(d["section_id"]) + ", Course ID:" + str(d["course_id"]))
        for lab in Lab.objects.all():
            d = lab.toDict()
            sections.append(
                d["section_type"] + "- Section ID:" + str(d["section_id"]) + ", Course ID:" + str(d["course_id"]))
        if len(sections) == 0:
            return render(request, "error.html", {"message": "No existing sections to delete",
                                                  "previous_url": "/home/managesection"})
        return render(request, "sectionManagement/delete_section.html", {"sections": sections})

    def post(self, request):
        curUserEmail = request.session["user"]
        curUserObj = AdminObj(Administrator(user=User.objects.get(email_address=curUserEmail)))
        formattedSecStr = request.POST["sections"]

        try:
            secObj = determineSec(formattedSecStr)  # sending string arg
            curUserObj.removeSection(secObj)
            return render(request, "success.html",
                          {"message": "Successfully Deleted Section", "previous_url": "/home/managesection/delete"})
        except Exception as e:
            return render(request, "error.html", {"message": e, "previous_url": "/home/managesection/delete"})


class EditSection(View):

    def get(self, request):
        # Ya know, probably should've just stuck with the map(str) :P
        sections = list()
        for lecture in Lecture.objects.all():
            d = lecture.toDict()
            sections.append(
                d["section_type"] + "- Section ID:" + str(d["section_id"]) + ", Course ID:" + str(d["course_id"]))
        for lab in Lab.objects.all():
            d = lab.toDict()
            sections.append(
                d["section_type"] + "- Section ID:" + str(d["section_id"]) + ", Course ID:" + str(d["course_id"]))
        if len(sections) == 0:
            return render(request, "error.html", {"message": "No existing sections to edit",
                                                  "previous_url": "/home/managesection"})
        return render(request, "sectionManagement/edit_section.html", {"sections": sections})

    def post(self, request):
        curUserEmail = request.session["user"]
        curUserObj = AdminObj(Administrator(user=User.objects.get(email_address=curUserEmail)))
        formattedSecStr = request.POST["sections"]

        try:
            secObj = determineSec(formattedSecStr)  # sending string arg
            id = int(request.POST.get("section_id")) #causing me lots of problems
            editInput = {"section_id": id,
                         "location": request.POST.get("location",),
                         "meeting_time": request.POST.get("meeting_time",)}
            curUserObj.editSection(secObj, editInput)
            return render(request, "success.html",
                          {"message": "Successfully Editted Section", "previous_url": "/home/managesection/edit"})
        except Exception as e:
            return render(request, "error.html", {"message": e, "previous_url": "/home/managesection/edit"})


class AddTAToSection(View):

    def get(self, request):
        return render(request, "sectionManagement/add_ta_to_section.html")


class Success(View):

    def get(self, request):
        return render(request, "success.html")


class Error(View):

    def get(self, request):
        return render(request, "success.html")
