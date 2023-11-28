from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

from TAScheduler.models import User, Administrator, Instructor, TA
from TAScheduler.views_methods import TAObj, InstructorObj, AdminObj


# Mostly temporary to get basic skeleton working
# TODO add post methods and make login screen default
# TODO fix the get methods to pass content information
# TODO make each page require correct session token to access

def determineUser(user):
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
        """Temp remove"""  # TODO remove
        request.session["user"] = "test@uwm.edu"
        """Temp remove"""
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
        if request.POST["phone_number"] == "":
            number = 0
        else:
            number = request.POST["phone_number"]
        account_info = {
            "email_address": request.POST["email_address"],
            "password": request.POST["password"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "home_address": request.POST["home_address"],
            "phone_number": number,
        }
        try:
            (AdminObj(Administrator.objects.get(user=User.objects.get(email_address=request.session.get("user")))).
             createUser(account_info, role=request.POST["role"]))
            return render(request, "success.html", {"message": "User successfully created",
                                                    "previous_url": "/home/manageaccount/create"})
        except TypeError:
            return render(request, "error.html", {"message": "Info not a dict",
                                                  "previous_url": "/home/manageaccount/create"})
        except RuntimeError:
            return render(request, "error.html", {"message": "User with email already exists",
                                                  "previous_url": "/home/manageaccount/create"})


class DeleteAccount(View):

    def get(self, request):
        users = list(map(str, Administrator.objects.all()))
        users.extend(list(map(str, Instructor.objects.all())))
        users.extend(list(map(str, TA.objects.all())))
        return render(request, "accountManagement/delete_account.html", {"users": users})

    def post(self, request):
        user_object = determineUser(request.POST["user"])
        try:
            AdminObj(Administrator.objects.get(user=User.objects.get(email_address=request.session.get("user")))).removeUser(user_object)
            return render(request, "success.html", {"message": "User successfully deleted",
                                                    "previous_url": "/home/manageaccount/delete"})
        except RuntimeError:
            return render(request, "error.html", {"message": "User does not exist",
                                                  "previous_url": "/home/manageaccount/delete"})
        except TypeError:
            return render(request, "error.html", {"message": "Input passed is not a subclass of user obj",
                                                  "previous_url": "home/manageaccount/delete"})


class EditAccount(View):

    def get(self, request):
        users = list(map(str, Administrator.objects.all()))
        users.extend(list(map(str, Instructor.objects.all())))
        users.extend(list(map(str, TA.objects.all())))
        return render(request, "accountManagement/edit_account.html", {"users": users,
                                                                       "selected": False, "role": "Admin"})

    def post(self, request):
        try:
            user_object = determineUser(request.POST["user"])
            role = user_object.getRole()
            request.session["current_edit"] = request.POST["user"]
            return render(request, "accountManagement/edit_account.html", {"users": None,
                                                                           "selected": True, "role": role})
        except MultiValueDictKeyError:
            grader = True
            if request.POST.get("grader_status") is None:
                grader = False
            account_info = {
                "email_address": request.POST.get("email_address"),
                "password": request.POST.get("password"),
                "first_name": request.POST.get("first_name"),
                "last_name": request.POST.get("last_name"),
                "home_address": request.POST.get("home_address"),
                "phone_number": int(request.POST.get("phone_number")),
                "grader_status": grader,
                "max_assignments": request.POST.get("max_assignments")
            }
            try:
                (AdminObj(Administrator.objects.get(user=User.objects.get(email_address=request.session.get("user"))))
                 .editUser(determineUser(request.session["current_edit"]), account_info))
                return render(request, "success.html", {"message": "User successfully changed",
                                                        "previous_url": "/home/manageaccount/edit"})
            except Exception as e:
                return render(request, "error.html", {"message": e,
                                                      "previous_url": "/home/manageaccount/edit"})


class SectionManagement(View):

    def get(self, request):
        return render(request, "sectionManagement/section_management.html")


class CreateSection(View):

    def get(self, request):
        return render(request, "sectionManagement/create_section.html")


class DeleteSection(View):
 # ad
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