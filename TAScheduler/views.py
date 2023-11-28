from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

from TAScheduler.models import User, Administrator, Instructor, TA
from TAScheduler.views_methods import TAObj, InstructorObj, AdminObj


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
        secs = ["Lab", "Lecture"]  # For dropdown
        return render(request, "sectionManagement/create_section.html", {"secs": secs})

    def post(self, request):
        curUserEmail = request.session["user_object"]  # should hold unique identifier "email"
        # Next sprint will require us to search for the user in the DB: current user may not be an admin
        curUserObj = AdminObj(Administrator(user=User.objects.get(email_address=curUserEmail)))

        section_id = request.POST.get('section_id')
        course_id = request.POST.get('course_id')
        section_type = request.POST.get('section_type')
        location = request.POST.get('location')
        meeting_time = request.POST.get('meeting_time')
        secInfo = {'section_id': section_id, 'course_id': course_id,
                   'section_type': section_type, 'location': location, 'meeting_time': meeting_time}
        try:
            curUserObj.createSection(secInfo)
            return render(request, "success.html", {"message": "Successfully Created " + section_type, "previous_url": "home/managesection/create"})
        except Exception as e:  # THIS TAKES THE MESSAGE INSIDE OF THE EXCEPTION AND STORES AS e, ValueError("me") <- "me"
            return render(request, "error.html", {"message": e, "previous_url": "home/managesection/create"})


class DeleteSection(View):

    def get(self, request):
        return render(request, "sectionManagement/delete_section.html")


class EditSection(View):

    def get(self, request):
        return render(request, "sectionManagement/edit_section.html")


class AddTAToSection(View):

    def get(self, request):
        return render(request, "sectionManagement/add_ta_to_section.html")
