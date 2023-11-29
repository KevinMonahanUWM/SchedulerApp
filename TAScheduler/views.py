from django.shortcuts import render
from django.views import View

from TAScheduler.models import TA, Instructor, Administrator, User, Lecture, Lab
from TAScheduler.views_methods import LectureObj, LabObj, TAObj, InstructorObj, AdminObj


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
        return render(request, "sectionManagement/create_section.html")


class DeleteSection(View):

    def get(self, request):
        return render(request, "sectionManagement/delete_section.html")


class EditSection(View):

    def get(self, request):
        return render(request, "sectionManagement/edit_section.html")


class AddUserToSection(View):

    def get(self, request):
        users = list(map(str, TA.objects.all()))
        users.extend(list(map(str, Instructor.objects.all())))
        if len(users) == 0:
            return render(request,
                          "error.html",
                          {"message": "No Users to display", "previous_url": "home/managesection"})

        return render(request, "sectionManagement/add_user_to_section.html",
                      {"users": users, "message": "Please select a user to assign"})

    def post(self, request):
        selecteduser = request.POST["user"]
        if selecteduser is None or selecteduser == '':
            users = request.POST["users"]
            return render(request,
                          "sectionManagement/add_user_to_section.html",
                          {"users": users,
                           "message": "Choose a User"})

        courses = None
        if isinstance(selecteduser, TA):
            if selecteduser.grader_status:
                courses = list(map(str, Lecture.objects.all()))
            else:
                courses = list(map(str, Lab.objects.all()))
        if isinstance(selecteduser, Instructor):
            courses = list(map(str, Lecture.objects.all()))

        if len(courses) == 0:
            return render(request,
                          "error.html",
                          {"message": "No Courses to display", "previous_url": "home/managesection"})

        chosenuser = determineUser(request.POST["user"]).getUsername()
        return render(request,
                      "sectionManagement/choose_section_add_user.html",
                      {"chosen": chosenuser, "courses": courses})


class ChooseSectionForUser(View):
    def get(self, request):
        if request.POST["course"].getLectureTAAsgmt is not None:
            return render(request,
                          "error.html",
                          {"message": "TA Is already assigned here", "previous_url": "home/managesection"})

        if isinstance(request.POST["course"], LectureObj):
            if not request.POST["chosen"].grader_status:
                return render(request,
                              "error.html",
                              {"message": "Non-Grader TA cannot be in a lecture", "previous_url": "home/managesection"})

        if isinstance(request.POST["course"], LabObj):
            if request.POST["chosen"].grader_status:
                return render(request,
                              "error.html",
                              {"message": "Grader TA cannot be in a lab", "previous_url": "home/managesection"})

        request.POST["course"].addTA(request.POST["chosen"])

        return render(request, "success.html", {"message": "TA successfully added",
                                                "previous_url": "home/managesection"})


class Success(View):

    def get(self, request):
        return render(request, "success.html")


class Error(View):

    def get(self, request):
        return render(request, "success.html")
