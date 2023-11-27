from django.shortcuts import render
from django.views import View

from TAScheduler.models import User, Administrator, Instructor, TA
from TAScheduler.views_methods import TAObj, InstructorObj, AdminObj


# Mostly temporary to get basic skeleton working
# TODO add post methods and make login screen default
# TODO fix the get methods to pass content information
# TODO make each page require correct session token to access


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
        roles = ["Admin", "Instructor", "TA"]
        return render(request, "accountManagement/create_account.html", {"roles": roles})

    def post(self, request):
        account_info = {
            "email_address": request.POST["email_address"],
            "password": request.POST["password"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "home_address": request.POST["home_address"],
            "phone_number": int(request.POST["phone_number"]),
        }
        try:
            request.session["user"].createUser(account_info, role=request.POST["role"])
            return render(request, "success.html", {"message": "User successfully created",
                                                    "previous_url": "/"})
        except:
            return render(request, "error.html", {"message": "Bad login information",
                                                  "previous_url": "/"})


class DeleteAccount(View):

    def get(self, request):
        """Temp remove"""  # TODO remove
        request.session["user"] = "test@uwm.edu"
        """Temp remove"""
        users = list(map(str, Administrator.objects.all()))
        users.extend(list(map(str, Instructor.objects.all())))
        users.extend(list(map(str, TA.objects.all())))
        return render(request, "accountManagement/delete_account.html", {"users": users})

    def post(self, request):
        email = request.POST["user"].split(": ", 1)[1]
        email_role = email.split(" -  ", 1)
        selected_user = User.objects.get(email_address=email_role[0])
        if email_role[1].lower() == "ta":
            user_object = TAObj(TA.objects.get(user=selected_user))
        elif email_role[1].lower() == "instructor":
            user_object = InstructorObj(Instructor.objects.get(user=selected_user))
        else:
            user_object = AdminObj(Administrator.objects.get(user=selected_user))
        try:
            AdminObj(Administrator.objects.get(user=User.objects.get(email_address=request.session["user"]))).removeUser(user_object)
            return render(request, "success.html", {"message": "User successfully deleted",
                                                    "previous_url": "home/manageaccount/delete"})
        except RuntimeError:
            return render(request, "error.html", {"message": "User does not exist",
                                                  "previous_url": "home/manageaccount/delete"})
        except TypeError:
            return render(request, "error.html", {"message": "Input passed is not a subclass of user obj",
                                                  "previous_url": "home/manageaccount/delete"})


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


class AddTAToSection(View):

    def get(self, request):
        return render(request, "sectionManagement/add_ta_to_section.html")

class Success(View):

    def get(self, request):
        return render(request, "success.html")


class Error(View):

    def get(self, request):
        return render(request, "success.html")