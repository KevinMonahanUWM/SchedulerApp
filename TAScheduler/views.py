from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

import TAScheduler
from TAScheduler.models import User, Administrator, Instructor, TA, Lecture, Lab
from TAScheduler.views_methods import TAObj, InstructorObj, AdminObj, LectureObj, LabObj


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

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_database = User.objects.get(email_address=username, password=password)
            if Administrator.objects.filter(user=user_database).exists():
                user = AdminObj(Administrator.objects.get(user=user_database))
            elif Instructor.objects.filter(user=user_database).exists():
                user = InstructorObj(Instructor.objects.get(user=user_database))
            elif TA.objects.filter(user=user_database).exists():
                user = TAObj(TA.objects.get(user=user_database))
            else:
                raise Exception("Bad password or username")
        except:
            return render(request, "login.html", {"error": "Invalid username or password"})

        if user.login(username, password):
            request.session["user"] = str(user.database)
            return redirect('/home/')


class Home(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        admin = False
        if determineUser(request.session["user"]).getRole() is "Admin":
            admin = True
        username = determineUser(request.session["user"]).getUsername()
        # Render the admin home page with context for navigation
        context = {
            'username': username,  # assuming the User model has a 'username' attribute
            'manage_accounts': '/home/manageaccount',
            'manage_courses': '/home/managecourse',
            'manage_sections': '/home/managesection',
            'role_admin': admin
        }
        return render(request, 'home.html', context)

    def post(self, request):

        # Perform actions based on the posted data
        # Assuming buttons in the admin_home.html have the name attribute set to these values
        if 'account_management' in request.POST:
            return redirect('/home/manageaccount')
        elif 'course_management' in request.POST:
            return redirect('/home/managecourse')
        elif 'section_management' in request.POST:
            return redirect('/home/managesection')
        elif 'logout' in request.POST:
            del request.session["user"]
            return redirect('/')  # Redirect to login page after logout
        else:
            # If the action is unrecognized, return to the home page with an error message
            return render(request, 'home.html', {'error': 'Unrecognized action'})


class CourseManagement(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "courseManagement/course_management.html")


class CreateCourse(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "courseManagement/create_course.html")


class DeleteCourse(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "courseManagement/delete_course.html")


class EditCourse(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "courseManagement/edit_course.html")


class AddInstructorToCourse(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "courseManagement/add_instructor_to_course.html")


class AccountManagement(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "accountManagement/account_management.html")


class CreateAccount(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
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
        print(request.session["user"])
        try:
            determineUser(request.session["user"]).createUser(account_info, role=request.POST["role"])
            return render(request, "success.html", {"message": "User successfully created",
                                                    "previous_url": "/home/manageaccount/create"})
        except Exception as e:
            return render(request, "error.html", {"message": e,
                                                  "previous_url": "/home/manageaccount/create"})


class DeleteAccount(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        users = list(
            map(str, Administrator.objects.exclude(user=determineUser(request.session["user"]).database.user)))
        users.extend(list(
            map(str, Instructor.objects.exclude(user=determineUser(request.session["user"]).database.user))))
        users.extend(
            list(map(str, TA.objects.exclude(user=determineUser(request.session["user"]).database.user))))
        if len(users) == 0:
            return render(request, "error.html", {"message": "No existing users to delete",
                                                  "previous_url": "/home/manageaccount/"})
        return render(request, "accountManagement/delete_account.html", {"users": users})

    def post(self, request):
        user_object = determineUser(request.POST["user"])
        try:
            determineUser(request.session["user"]).removeUser(user_object)
            return render(request, "success.html", {"message": "User successfully deleted",
                                                    "previous_url": "/home/manageaccount/delete/"})
        except Exception as e:
            return render(request, "error.html", {"message": e,
                                                  "previous_url": "/home/manageaccount/delete/"})


class EditAccount(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        users = list(
            map(str, Administrator.objects.exclude(user=determineUser(request.session["user"]).database.user)))
        users.extend(list(
            map(str, Instructor.objects.exclude(user=determineUser(request.session["user"]).database.user))))
        users.extend(
            list(map(str, TA.objects.exclude(user=determineUser(request.session["user"]).database.user))))
        if len(users) == 0:
            return render(request, "error.html", {"message": "No existing users to edit",
                                                  "previous_url": "/home/manageaccount"})
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
            if request.POST["phone_number"] == "":
                number = 0
            else:
                number = request.POST["phone_number"]
            grader = True
            if request.POST.get("grader_status") is None or request.POST.get("grader_status") is "":
                grader = False
            account_info = {
                "email_address": request.POST.get("email_address"),
                "password": request.POST.get("password"),
                "first_name": request.POST.get("first_name"),
                "last_name": request.POST.get("last_name"),
                "home_address": request.POST.get("home_address"),
                "phone_number": number,
                "grader_status": grader,
                "max_assignments": request.POST.get("max_assignments")
            }
            try:
                determineUser(request.session["user"]).editUser(determineUser(request.session["current_edit"]),
                                                                account_info)
                del request.session["current_edit"]
                return render(request, "success.html", {"message": "User successfully changed",
                                                        "previous_url": "/home/manageaccount/edit"})
            except Exception as e:
                del request.session["current_edit"]
                return render(request, "error.html", {"message": e,
                                                      "previous_url": "/home/manageaccount/edit"})


class SectionManagement(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "sectionManagement/section_management.html")


class CreateSection(View):
    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "sectionManagement/create_section.html")

    def post(self, request):
        section_id = request.POST.get('section_id')
        course_id = request.POST.get('course_id')
        section_type = request.POST.get('section_type')
        location = request.POST.get('location')
        meeting_time = request.POST.get('meeting_time')
        secInfo = {'section_id': section_id, 'course_id': course_id,
                   'section_type': section_type, 'location': location, 'meeting_time': meeting_time}

        adminUser = request.session["user_object"]  # ASSUMING WE'RE STORING AdminObj IN SESSION AT THE LOGIN
        try:
            # ASSUMING .createSection() WILL HANDLE ALL THE BAD INPUT.
            # WE'RE GOING TO NEED TO ADJUST ALL OUR MESSAGES TO RETURN MESSAGES NOT JUST THROW EXCEPTIONS
            # ... UNLESS MAKE CUSTOM EXCEPTIONS AND CHECK FOR THOSE HERE?
            message = adminUser.createSection(secInfo)
            # WE DON'T HAVE SUCCESS URL OR SUCCESS HTML ATM.
            return render(request, "success.html", {"message": message})
        except Exception as e:
            # WE DON'T HAVE ERROR URL OR ERROR HTML ATM.
            # NEED A WAY TO RETURN AN INFORMATIVE MESSAGE FROM THE CREATESECTION METHOD
            return render(request, "error.html", {"message": e})


class DeleteSection(View):
    # ad
    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "sectionManagement/delete_section.html")


class EditSection(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        return render(request, "sectionManagement/edit_section.html")


class AddUserToSection(View):

    def get(self, request):
        users = list(map(str, TA.objects.all()))
        users.extend(list(map(str, Instructor.objects.all())))
        if len(users) == 0:
            return render(request,
                          "error.html",
                          {"message": "No Users to display", "previous_url": "/home/managesection/"})

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
                          {"message": "No Courses to display", "previous_url": "/home/managesection/"})

        chosenuser = determineUser(request.POST["user"]).getUsername()
        return render(request,
                      "sectionManagement/choose_section_add_user.html",
                      {"chosen": chosenuser, "courses": courses})


class ChooseSectionForUser(View):
    def get(self, request):
        #
        chosenuser = request.POST["chosen"]
        chosencourse = request.POST["course"]
        if chosencourse is None:
            courses = request.POST["courses"]
            return render(request,
                          "sectionManagement/choose_section_add_user.html",
                          {"chosen": chosenuser,
                           "courses": courses,
                           "message": "Choose a course"})

        user_database = User.objects.get(email_address=request.POST["username"])
        if isinstance(chosencourse, Lecture):
            chosencourse = LectureObj(chosencourse)
            if Instructor.user.objects.filter(email_address=chosenuser).exists():
                user = Instructor.objects.get(user=user_database)
                chosencourse.addInstr(user)
            elif TA.user.objects.filter(email_address=chosenuser).exists():
                user = TA.objects.get(user=user_database)
                chosencourse.addTA(user)
            else:
                return render(request, "error.html", {"message": "Could not find user",
                                                      "previous_url": "/home/managesection/"})

        if isinstance(chosencourse, Lab):
            chosencourse = LabObj(chosencourse)
            if TA.user.objects.filter(email_address=chosenuser).exists():
                user = TA.objects.get(user=user_database)
                chosencourse.addTA(user)
            else:
                return render(request, "error.html", {"message": "Could not find user",
                                                      "previous_url": "/home/managesection/"})

        return render(request, "success.html", {"message": "TA successfully added",
                                                "previous_url": "/home/managesection/"})


class Success(View):

    def get(self, request):
        return render(request, "success.html")


class Error(View):

    def get(self, request):
        return render(request, "success.html")


class Forgot_Password(View):

    def get(self, request):
        return render(request, "forgot_password.html", {"recievedUser": False})

    def post(self, request):
        try:
            user_database = User.objects.get(email_address=request.POST["username"])
            if Administrator.objects.filter(user=user_database).exists():
                user = AdminObj(Administrator.objects.get(user=user_database))
            elif Instructor.objects.filter(user=user_database).exists():
                user = InstructorObj(Instructor.objects.get(user=user_database))
            elif TA.objects.filter(user=user_database).exists():
                user = TAObj(TA.objects.get(user=user_database))
            else:
                raise Exception
            request.session["current_edit"] = str(user.database)
            return render(request, "forgot_password.html", {"recievedUser": True})
        except TAScheduler.models.User.DoesNotExist:
            return render(request, "forgot_password.html", {"recievedUser": False, "message": "Invalid email address"})

        except MultiValueDictKeyError:
            account_info = {
                "password": request.POST.get("password"),
            }
            try:
                admin_user_info = User.objects.create(
                    email_address="admin@example.com",
                    password="admin_pass",
                    first_name="Admin",
                    last_name="User",
                    home_address="123 Admin Street",
                    phone_number=1234567890
                )
                admin_model = Administrator.objects.create(user=admin_user_info)
                adminObj = AdminObj(admin_model)
                adminObj.editUser(determineUser(request.session["current_edit"]), account_info)
                del request.session["current_edit"]
                User.delete(admin_model)
                return render(request, "success.html", {"message": "Successfully changed password",
                                                        "previous_url": "/"})
            except Exception as e:
                del request.session["current_edit"]
                return render(request, "error.html", {"message": e,
                                                      "previous_url": "/"})
