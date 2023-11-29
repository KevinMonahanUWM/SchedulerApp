from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

import TAScheduler
from TAScheduler.models import User, Administrator, Instructor, TA, Lecture, Lab, Section, Course
from TAScheduler.views_methods import TAObj, InstructorObj, AdminObj, LabObj, LectureObj, CourseObj


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


# Sending in format: "Lecture- Section ID:#, Course ID:#"
def determineSec(section):
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
            'manage_accounts': '/home/manageaccount/',
            'manage_courses': '/home/managecourse/',
            'manage_sections': '/home/managesection/',
            'role_admin': admin
        }
        return render(request, 'home.html', context)

    def post(self, request):
        if 'logout' in request.POST:
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

    def post(self, request):
        # Handle the creation of a course based on form data
        course_info = {
            "course_id": request.POST.get("course_id"),
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "num_of_sections": int(request.POST.get("num_of_sections")),
            "modality": request.POST.get("modality"),
            "credits": int(request.POST.get("credits")),
            "semester": request.POST.get("semester")
        }
        try:
            determineUser(request.session["user"]).createCourse(course_info)
            return render(request, "success.html", {"message": "User successfully created",
                                                    "previous_url": "/home/managecourse/create/"})
        except Exception as e:
            # Handle any exceptions, possibly show an error page
            return render(request, "error.html", {"message": str(e)})


class DeleteCourse(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        courses = Course.objects.all()
        return render(request, "courseManagement/delete_course.html")


    def post(self, request):
        course_id = request.POST.get('course_id')

        try:
            course_to_delete = Course.objects.get(id=course_id)
            course_obj = CourseObj(course_to_delete)
            course_obj.removeCourse()
            return redirect('/path/to/success/page')
        except Course.DoesNotExist:
            return render(request, "error.html", {"message": "Course not found"})
        except Exception as e:
            return render(request, "error.html", {"message": str(e)})


class EditCourse(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        courses = Course.objects.all()
        return render(request, "courseManagement/edit_course.html")

    def post(self, request):
        course_id = request.POST.get('course_id')
        new_info = {
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "num_of_sections": int(request.POST.get("num_of_sections")),
            "modality": request.POST.get("modality"),
            "credits": int(request.POST.get("credits")),
            "semester": request.POST.get("semester")
        }

        try:
            course_to_edit = Course.objects.get(id=course_id)
            course_obj = CourseObj(course_to_edit)
            course_obj.editCourse(new_info)
            return redirect('/path/to/success/page')
        except Course.DoesNotExist:
            return render(request, "error.html", {"message": "Course not found"})
        except Exception as e:
            return render(request, "error.html", {"message": str(e)})


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
                                                    "previous_url": "/home/manageaccount/create/"})
        except Exception as e:
            return render(request, "error.html", {"message": e,
                                                  "previous_url": "/home/manageaccount/create/"})


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
                                                  "previous_url": "/home/manageaccount/"})
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
                                                        "previous_url": "/home/manageaccount/edit/"})
            except Exception as e:
                del request.session["current_edit"]
                return render(request, "error.html", {"message": e,
                                                      "previous_url": "/home/manageaccount/edit/"})


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
                                                    "previous_url": "/home/managesection/create/"})
        except Exception as e:  # THIS TAKES THE MESSAGE INSIDE OF THE EXCEPTION AND STORES AS e, ValueError("me") <- "me"
            return render(request, "error.html", {"message": e, "previous_url": "/home/managesection/create/"})


class DeleteSection(View):
    # ad
    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
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
                                                  "previous_url": "/home/managesection/"})
        return render(request, "sectionManagement/delete_section.html", {"sections": sections})

    def post(self, request):
        curUserEmail = request.session["user"]
        curUserObj = AdminObj(Administrator(user=User.objects.get(email_address=curUserEmail)))
        formattedSecStr = request.POST["sections"]

        try:
            secObj = determineSec(formattedSecStr)  # sending string arg
            curUserObj.removeSection(secObj)
            return render(request, "success.html",
                          {"message": "Successfully Deleted Section", "previous_url": "/home/managesection/delete/"})
        except Exception as e:
            return render(request, "error.html", {"message": e, "previous_url": "/home/managesection/delete/"})


class EditSection(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        sections = list(map(str, Lecture.objects.all()))  # lectures
        sections.extend(map(str, Lab.objects.all()))  # labs
        if len(sections) == 0:
            return render(request, "error.html", {"message": "No existing sections to edit",
                                                  "previous_url": "/home/managesection/"})
        return render(request, "sectionManagement/edit_section.html", {"sections": sections})

    def post(self, request):
        curUserEmail = request.session["user_object"]
        curUserObj = AdminObj(Administrator(user=User.objects.get(email_address=curUserEmail)))
        sectionType = request.POST["section"]
        secObj = determineSec(sectionType)  # sending string arg

        try:
            curUserObj.editSection(secObj)
            return render(request, "success.html",
                          {"message": "Successfully Editted Section", "previous_url": "/home/managesection/edit/"})
        except Exception as e:
            return render(request, "error.html", {"message": e, "previous_url": "/home/managesection/edit/"})


class AddTAToSection(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() is not "Admin":
            return redirect("/home/")
        users = list(map(str, TA.objects.all()))
        if len(users) == 0:
            return render(request,
                          "error.html",
                          {"message": "No TAs to display", "previous_url": "/home/managesection/"})

        return render(request, "sectionManagement/add_ta_to_section.html", {"users": users})

    def post(self, request):
        if request.POST["ta"] == "":
            users = request.POST["users"]
            return render(request,
                          "sectionManagement/add_ta_to_section.html",
                          {"users": users,
                           "message": "Choose a TA"})

        courses = list(map(str, Lecture.objects.all().getID()))
        courses.extend(list(map(str, Lab.objects.all().getID())))
        if len(courses) == 0:
            return render(request,
                          "error.html",
                          {"message": "No Courses to display", "previous_url": "/home/managesection/"})

        chosenuser = request.POST["ta"].user.email_address
        return render(request,
                      "sectionManagement/add_ta_to_section.html",
                      {"chosen": chosenuser, "courses": courses})


class AddTAToSectionSuccess(View):
    def get(self, request):
        if request.POST["course"].getLectureTAAsgmt is not None:
            return render(request,
                          "error.html",
                          {"message": "TA Is already assigned here", "previous_url": "home/managesection/"})

        if isinstance(request.POST["course"], LectureObj):
            if not request.POST["chosen"].grader_status:
                return render(request,
                              "error.html",
                              {"message": "Non-Grader TA cannot be in a lecture",
                               "previous_url": "home/managesection/"})

        if isinstance(request.POST["course"], LabObj):
            if request.POST["chosen"].grader_status:
                return render(request,
                              "error.html",
                              {"message": "Grader TA cannot be in a lab", "previous_url": "home/managesection/"})

        request.POST["course"].addTA(request.POST["chosen"])

        return render(request, "success.html", {"message": "TA successfully added",
                                                "previous_url": "home/managesection/"})


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
