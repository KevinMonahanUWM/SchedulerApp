from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

import TAScheduler
from TAScheduler.models import User, Administrator, Instructor, TA, Section, Lab, Lecture, Course, InstructorToCourse, \
    TAToCourse
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


def determineSec(section):  # Take "formatted str", return lab/lec obj.
    secInfo = section.split("- ", 1)  # Ex: (Lecture)[0] & (Section ID:#, Course ID:#)[1]
    sectionInf = secInfo[0].split(":")
    secID = int(sectionInf[1])  # Ex: (Section ID)[0] & (#)[1]
    try:
        secDB = Section.objects.get(section_id=secID)
        if sectionInf[0] == "Lab":
            secObj = LabObj(Lab.objects.get(section=secDB))
        else:  # if not lab assuming it's a lecture
            secObj = LectureObj(Lecture.objects.get(section=secDB))
        return secObj
    except:
        raise RuntimeError("Section does not exist in Database")


def coursesAddAssignments():
    courseAndUsers = []
    instructors = Instructor.objects.all()
    tas = TA.objects.all()
    for course in Course.objects.all():
        users = []
        for instruc in instructors:
            if (not InstructorObj(instruc).hasMaxAsgmts() and
                    not InstructorToCourse.objects.filter(course=course, instructor=instruc).exists()):
                users.append(str(instruc))
        for ta in tas:
            if not TAObj(ta).hasMaxAsgmts() and not TAToCourse.objects.filter(ta=ta, course=course).exists():
                users.append(str(ta))
        courseAndUsers.append({"course": str(course), "users": users})
    return courseAndUsers


def usersCurrentlyAvailable(courseList, course):
    for courseName in courseList:
        if courseName.get("course") == course:
            return courseName.get("users")


def currentlyAssignedUsers(course_id):
    assignments = CourseObj(Course.objects.get(course_id=course_id)).getAsgmtsForCrse()
    users = []
    for instrc in assignments.get("instructors"):
        users.append(str(instrc.instructor))
    for ta in assignments.get("tas"):
        if ta.ta.grader_status:
            users.append(str(ta.ta))
    return users


def currentlyAssignedUsersLab(course_id):
    assignments = CourseObj(Course.objects.get(course_id=course_id)).getAsgmtsForCrse()
    users = []
    for ta in assignments.get("tas"):
        if not ta.ta.grader_status:
            users.append(str(ta.ta))
    return users


def usersInSection(secObj):
    users = []
    if isinstance(secObj, LabObj):
        if secObj.getLabTAAsgmt() is not None:
            users.append(str(secObj.getLabTAAsgmt()))
    else:
        if secObj.getLecInstrAsmgt() is not None:
            users.append(str(secObj.getLecInstrAsmgt()))
        if secObj.getLectureTAAsgmt() is not None:
            users.append(str(secObj.getLectureTAAsgmt()))
    return users


def usersInCourseNotSec(courseUsers, sectionUsers):
    unattached = []
    if len(sectionUsers) == 0:
        unattached = courseUsers
    else:
        for user in courseUsers:
            if user not in sectionUsers:
                unattached.append(user)
    return unattached


def allUsers():
    users = list(map(str, Administrator.objects.all()))
    users.extend(list(map(str, Instructor.objects.all())))
    users.extend(list(map(str, TA.objects.all())))
    return users


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            print(list(map(str, User.objects.all())))
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
        role = determineUser(request.session["user"]).getRole()
        username = determineUser(request.session["user"]).getUsername()
        # Render the admin home page with context for navigation
        courseExist = True
        if len(Course.objects.all()) == 0:
            courseExist = False
        context = {
            'role_name': determineUser(request.session["user"]).getRole(),
            'username': username,  # assuming the User model has a 'username' attribute
            'manage_accounts': '/home/manageaccount',
            'manage_courses': '/home/managecourse',
            'manage_sections': '/home/managesection',
            'courses_exists': courseExist
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
        courseWithUsers = coursesAddAssignments()
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() != "Admin":
            return redirect("/home/")
        return render(request, "courseManagement/course_management.html", {"courses": courseWithUsers})

    def post(self, request):
        courses = coursesAddAssignments()
        course = request.POST.get('course')
        course_id = int(course.split(": ", 1)[0])
        if request.POST.get("edit") is not None:
            request.session["course_id"] = course_id
            selected_course = Course.objects.get(course_id=course_id)
            return render(request, "courseManagement/edit_course.html",
                          {"selected": True, "selected_course": selected_course})
        elif request.POST.get("delete") is not None:
            curUserObj = determineUser(request.session["user"])
            try:
                course_to_delete = CourseObj(Course.objects.get(course_id=course_id))
                curUserObj.removeCourse(course_to_delete)
                courses = coursesAddAssignments()
                return render(request, "courseManagement/course_management.html",
                              {"message": "Successfully deleted course", "courses": courses})
            except Exception as e:
                return render(request, "courseManagement/course_management.html",
                              {"message": str(e), "courses": courses})
        elif request.POST.get("details") is not None:
            course_id = int(course.split(": ", 1)[0])
            course_instance = Course.objects.get(course_id=course_id)
            course_obj = CourseObj(course_instance)  # Wrap the course instance
            course_info = course_obj.getCrseInfo()
            usersCurrentlyAssigned = currentlyAssignedUsers(course_id)
            noneAssigned = len(usersCurrentlyAssigned) == 0
            usersAvailableToAssign = usersCurrentlyAvailable(coursesAddAssignments(), course)
            noneAvailable = len(usersAvailableToAssign) == 0
            return render(request, "courseManagement/course_user_assignments.html",
                          {"course": course, "course_info": course_info, "assignedEmpty": noneAssigned,
                           "unassignedEmpty": noneAvailable, "assigned": usersCurrentlyAssigned,
                           "unassigned": usersAvailableToAssign})


class CreateCourse(View):
    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() != "Admin":
            return redirect("/home/")
        return render(request, "courseManagement/create_course.html")

    def post(self, request):
        admin_obj = determineUser(request.session["user"])

        course_info = {
            "course_id": request.POST.get("course_id"),
            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "num_of_sections": int(request.POST.get("num_of_sections")),
            "modality": request.POST.get("modality"),
            "semester": request.POST.get("semester")
        }

        # Check if course already exists
        if Course.objects.filter(course_id=course_info["course_id"]).exists():
            return render(request, "courseManagement/create_course.html",
                          {"message": "A course with this ID already exists"})

        try:
            admin_obj.createCourse(course_info)
            courses = coursesAddAssignments()
            return render(request, "courseManagement/course_management.html",
                          {"message": "Successfully created course", "courses": courses})
        except Exception as e:
            return render(request, "courseManagement/create_course.html",
                          {"message": str(e)})


class EditCourse(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() != "Admin":
            return redirect("/home/")
        return redirect("/home/managecourse")

    def post(self, request):
        admin_obj = determineUser(request.session["user"])

        new_info = {

            "name": request.POST.get("name"),
            "description": request.POST.get("description"),
            "num_of_sections": int(request.POST.get("num_of_sections", 0)),  # Default to 0 or any sensible default
            "modality": request.POST.get("modality"),
            "semester": request.POST.get("semester")
        }
        try:
            course_id = request.session["course_id"]
            course_to_edit = Course.objects.get(course_id=course_id)
            del request.session["course_id"]
            admin_obj.editCourse(CourseObj(course_to_edit), new_info)
            courses = coursesAddAssignments()
            return render(request, "courseManagement/course_management.html", {"message": "Successfully editted course",
                                                                               "courses": courses})
        except Course.DoesNotExist:
            courses = coursesAddAssignments()
            return render(request, "courseManagement/course_management.html",
                          {"message": "Course not found", "courses": courses})
        except Exception as e:
            courses = coursesAddAssignments()
            return render(request, "courseManagement/course_management.html",
                          {"message": str(e), "courses": courses})


class CourseUserAssignments(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() != "Admin":
            return redirect("/home/")
        return redirect("/home/managecourse")

    def post(self, request):
        selecteduser = determineUser(request.POST.get("user"))
        course_id = int(request.POST.get('course').split(": ", 1)[0])
        courseobj = CourseObj(Course.objects.get(course_id=course_id))
        if request.POST.get("unassign") is not None:
            try:
                courseobj.removeAssignment(selecteduser)
                courses = coursesAddAssignments()
                return render(request, "courseManagement/course_management.html",
                              {"message": "Successfully removed assignment", "courses": courses})
            except Exception as e:
                courses = coursesAddAssignments()
                return render(request, "courseManagement/course_management.html",
                              {"message": str(e), "courses": courses})
        else:
            try:
                if selecteduser.getRole() == 'TA':
                    courseobj.addTa(selecteduser)
                else:
                    courseobj.addInstructor(selecteduser)
                courses = coursesAddAssignments()
                return render(request, "courseManagement/course_management.html",
                              {"message": "Successfully assigned user to course", "courses": courses})
            except Exception as e:
                courses = coursesAddAssignments()
                return render(request, "courseManagement/course_management.html",
                              {"message": str(e), "courses": courses})


class AccountManagement(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        users = allUsers()
        return render(request, "accountManagement/account_management.html",
                      {"users": users, "current_user": request.session.get("user"), "role":
                          determineUser(request.session["user"]).getRole()})

    def post(self, request):
        if request.POST.get("edit") is not None:
            role = determineUser(request.POST.get("user")).getRole()
            request.session["current_edit"] = request.POST["user"]
            user = determineUser(request.POST.get("user")).database
            return render(request, "accountManagement/edit_account.html", {"role": role, "user": user,
                                                        "user_role": determineUser(request.session["user"]).getRole()})
        else:
            try:
                determineUser(request.session["user"]).removeUser(determineUser(request.POST.get("user")))
                users = allUsers()
                return render(request, "accountManagement/account_management.html",
                              {"users": users, "current_user": request.session.get("user"),
                               "message": "User successfully deleted"})
            except Exception as e:
                users = allUsers()
                return render(request, "accountManagement/account_management.html",
                              {"users": users, "current_user": request.session.get("user"),
                               "message": e})


class CreateAccount(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() != "Admin":
            return redirect("/home/")
        roles = ["Admin", "Instructor", "TA"]
        return render(request, "accountManagement/create_account.html", {"roles": roles})

    def post(self, request):
        role = determineUser(request.session["user"]).getRole()
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
            if determineUser(request.session["user"]).getRole() == "TA":
                determineUser(request.session["user"]).setSkills(request.POST["skills"])
            determineUser(request.session["user"]).createUser(account_info, role=request.POST["role"])
            users = allUsers()
            return render(request, "accountManagement/account_management.html",
                          {"users": users, "current_user": request.session.get("user"),
                           "message": "Successfully created account", "role": role})
        except Exception as e:
            roles = ["Admin", "Instructor", "TA"]
            return render(request, "accountManagement/create_account.html",
                          {"message": str(e), "roles": roles})


class EditAccount(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        return redirect("/home/manageaccount")

    def post(self, request):
        if request.POST["phone_number"] == "":
            number = 0
        else:
            number = request.POST["phone_number"]
        grader = True
        if request.POST.get("grader_status") is None or request.POST.get("grader_status") == "":
            grader = False
        if request.POST.get("max_assignments") is None or request.POST.get("max_assignments") == "":
            max = 0
        else:
            max = int(request.POST.get("max_assignments"))
        account_info = {
            "email_address": request.POST.get("email_address"),
            "password": request.POST.get("password"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "home_address": request.POST.get("home_address"),
            "phone_number": number,
            "grader_status": grader,
            "max_assignments": max
        }
        try:
            role = determineUser(request.session["current_edit"]).getRole()
            if role == "TA":
                determineUser(request.session["current_edit"]).setSkills(request.POST.get("skills"))
            if determineUser(request.session["user"]).getRole() != "Admin":
                admin_user_info = User.objects.create(
                    email_address="admin@exampledontuse.com",
                    password="admin_pass",
                    first_name="Admin",
                    last_name="User",
                    home_address="123 Admin Street",
                    phone_number=1234567890
                )
                admin_model = Administrator.objects.create(user=admin_user_info)
                adminObj = AdminObj(admin_model)
                adminObj.editUser(determineUser(request.session["current_edit"]), account_info)
                request.session["user"] = str(determineUser(request.session["user"]).database)
                del request.session["current_edit"]
                User.delete(admin_model)
                users = allUsers()
                return render(request, "accountManagement/account_management.html",
                              {"users": users, "current_user": request.session.get("user"),
                               "message": "User successfully edited", "role": role})
            else:
                determineUser(request.session["user"]).editUser(determineUser(request.session["current_edit"]),
                                                                account_info)

            if request.session["current_edit"] == request.session["user"] and request.POST.get(
                    "email_address") is not None:
                request.session["user"] = str(Administrator.objects.get(
                    user__email_address=request.POST.get("email_address")))
            elif request.session["current_edit"] == request.session["user"]:
                request.session["user"] = str(Administrator.objects.get(
                    user__email_address=determineUser(request.session["user"]).getUsername()))
            del request.session["current_edit"]
            users = allUsers()
            return render(request, "accountManagement/account_management.html",
                          {"users": users, "current_user": request.session.get("user"),
                           "message": "User successfully edited", "role": role})
        except Exception as e:
            user = determineUser(request.session["current_edit"]).database
            return render(request, "accountManagement/edit_account.html",
                          {"message": e, "role": role, "user": user,
                           "user_role": determineUser(request.session["user"]).getRole()})


class SectionManagement(View):

    def get(self, request):
        if len(Course.objects.all()) == 0:
            return redirect("/home/")
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() != "Admin":
            return redirect("/home/")
        sections = list(map(str, Lecture.objects.all()))
        sections.extend(list(map(str, Lab.objects.all())))
        return render(request, "sectionManagement/section_management.html", {"sections": sections})

    def post(self, request):
        if request.POST.get("edit") is not None:
            request.session["current_edit"] = request.POST.get("section")
            section = determineSec(request.session.get("current_edit")).database
            return render(request, "sectionManagement/edit_section.html", {"selected": True,
                                                                           "section": section})
        elif request.POST.get("delete") is not None:
            curUserObj = determineUser(request.session["user"])
            secObj = determineSec(request.POST.get("section"))
            try:
                curUserObj.removeSection(secObj)
                sections = list(map(str, Lecture.objects.all()))
                sections.extend(list(map(str, Lab.objects.all())))
                return render(request, "sectionManagement/section_management.html",
                              {"message": "Successfully Deleted Section", "sections": sections})
            except Exception as e:
                sections = list(map(str, Lecture.objects.all()))
                sections.extend(list(map(str, Lab.objects.all())))
                return render(request, "sectionManagement/section_management.html",
                              {"message": e, "sections": sections})
        else:
            secObj = determineSec(request.POST.get("section"))
            courseObj = CourseObj(secObj.getParentCourse())
            if isinstance(secObj, LabObj):
                usersInCourse = currentlyAssignedUsersLab(courseObj.getCrseInfo().get("course_id"))
            else:
                usersInCourse = currentlyAssignedUsers(courseObj.getCrseInfo().get("course_id"))
            attachedUsers = usersInSection(secObj)
            unattachedUsers = usersInCourseNotSec(usersInCourse, attachedUsers)
            noneAssigned = False
            if len(attachedUsers) == 0:
                noneAssigned = True
            noneAvailable = False
            if len(unattachedUsers) == 0:
                noneAvailable = True
            return render(request, "sectionManagement/section_user_assignment.html",
                          {"section": request.POST.get("section"), "assignedEmpty": noneAssigned,
                           "unassignedEmpty": noneAvailable, "assigned": attachedUsers, "unassigned": unattachedUsers})


class CreateSection(View):
    def get(self, request):
        if len(Course.objects.all()) == 0:
            return redirect("/home/")
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() != "Admin":
            return redirect("/home/")
        secs = ["Lab", "Lecture"]  # For dropdown
        courses = Course.objects.all()
        return render(request, "sectionManagement/create_section.html", {"secs": secs, "courses": courses})

    def post(self, request):  #
        # Next sprint will require us to search for the user in the DB: current user may not be an admin
        curUserObj = determineUser(request.session["user"])
        course_id = request.POST.get('course_id')
        section_id = request.POST.get('section_id')
        section_type = request.POST.get('section_type')
        meeting_time = request.POST.get('meeting_time')
        location = request.POST.get('location')

        secInfo = {'course_id': course_id, 'section_id': section_id,
                   'section_type': section_type, 'meeting_time': meeting_time, 'location': location}
        try:
            curUserObj.createSection(secInfo)
            sections = list(map(str, Lecture.objects.all()))
            sections.extend(list(map(str, Lab.objects.all())))
            return render(request, "sectionManagement/section_management.html",
                          {"message": "Successfully Created Section", "sections": sections})
        except Exception as e:
            secs = ["Lab", "Lecture"]  # For dropdown
            courses = Course.objects.all()
            return render(request, "sectionManagement/create_section.html",
                          {"message": e, "secs": secs, "courses": courses})


class EditSection(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() != "Admin":
            return redirect("/home/")
        return redirect("/home/managesection")

    def post(self, request):
        curUserObj = determineUser(request.session["user"])
        secObj = determineSec(request.session.get("current_edit"))  # sending string arg
        editInput = {"section_id": int(request.POST.get("section_id")),
                     "location": request.POST.get("location", ),
                     "meeting_time": request.POST.get("meeting_time", )}
        try:
            curUserObj.editSection(secObj, editInput)
            del request.session["current_edit"]
            sections = list(map(str, Lecture.objects.all()))
            sections.extend(list(map(str, Lab.objects.all())))
            return render(request, "sectionManagement/section_management.html",
                          {"message": "Successfully Editted Section", "sections": sections})
        except Exception as e:
            return render(request, "sectionManagement/edit_section.html",
                          {"message": e, "selected": True, "section": secObj.database})


class SectionUserAssignment(View):

    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")
        if determineUser(request.session["user"]).getRole() != "Admin":
            return redirect("/home/")
        return redirect("/home/managesection")

    def post(self, request):
        curUserObj = determineUser(request.POST.get("user"))
        role = curUserObj.getRole()
        secObj = determineSec(request.POST.get("section"))
        if request.POST.get("unassign") is not None:
            try:
                if isinstance(secObj, LabObj):
                    secObj.removeTA()
                else:
                    if role == "TA":
                        secObj.removeTA()
                    else:
                        secObj.removeInstr()
                sections = list(map(str, Lecture.objects.all()))
                sections.extend(list(map(str, Lab.objects.all())))
                return render(request, "sectionManagement/section_management.html",
                              {"message": "Successfully removed user", "sections": sections})
            except Exception as e:
                sections = list(map(str, Lecture.objects.all()))
                sections.extend(list(map(str, Lab.objects.all())))
                return render(request, "sectionManagement/section_management.html",
                              {"message": str(e), "sections": sections})
        else:
            try:
                if isinstance(secObj, LabObj):
                    secObj.addTA(curUserObj.database)
                else:
                    if role == "TA":
                        secObj.addTA(curUserObj.database)
                    else:
                        secObj.addInstr(curUserObj.database)
                sections = list(map(str, Lecture.objects.all()))
                sections.extend(list(map(str, Lab.objects.all())))
                return render(request, "sectionManagement/section_management.html",
                              {"message": "Successfully added user", "sections": sections})
            except Exception as e:
                sections = list(map(str, Lecture.objects.all()))
                sections.extend(list(map(str, Lab.objects.all())))
                return render(request, "sectionManagement/section_management.html",
                              {"message": str(e), "sections": sections})


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
                return render(request, "forgot_password.html", {"message": "Successfully changed password",
                                                                "recievedUser": False})
            except Exception as e:
                del request.session["current_edit"]
                return render(request, "forgot_password.html", {"message": e,
                                                                "recievedUser": False})


class ViewTAAssignments(View):
    def get(self, request):
        if request.session.get("user") is None:
            return redirect("/")

        # Logic to fetch TA assignments
        ta_assignments = []  # Replace with actual logic to fetch assignments
        for ta in TA.objects.all():
            for course in TAToCourse.objects.filter(ta=ta):
                ta_assignments.append({
                    'ta_name': ta.getName(),
                    'course_name': course.course.name,
                    'section_id': course.course.section_id
                })

        return render(request, 'ta_assignments.html', {'ta_assignments': ta_assignments})
