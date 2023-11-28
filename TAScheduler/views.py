from django.shortcuts import render, redirect
from django.views import View
from TAScheduler.models import User, Administrator, Instructor, TA
from TAScheduler.views_methods import TAObj, InstructorObj, AdminObj
from django.urls import reverse

# Mostly temporary to get basic skeleton working
# TODO add post methods and make login screen default
# TODO fix the get methods to pass content information
# TODO make each page require correct session token to access


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = None
        if Administrator.objects.filter(user__email_address=username).exists():
            admin_info = Administrator.objects.get(user__email_address=username)
            user = AdminObj(admin_info)
        elif TA.objects.filter(user__email_address=username).exists():
            ta_info = TA.objects.get(user__email_address=username)
            user = TAObj(ta_info)
        elif Instructor.objects.filter(user__email_address=username).exists():
            instr_info = Instructor.objects.get(user__email_address=username)
            user = InstructorObj(instr_info)

        if user and user.login(username, password):
            return redirect('/home/')
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

class Home(View):

    def get(self, request):
        if not request.user.login:
            return redirect('/login/')

        # Render the admin home page with context for navigation
        context = {
            'username': request.user.username,  # assuming the User model has a 'username' attribute
            'manage_accounts_url': '/home/manageaccount',
            'manage_courses_url': '/home/managecourse',
            'manage_sections_url': '/home/managesection',
        }
        return render(request, 'admin_home.html', context)

    def post(self, request):
        if not request.user.login:
            return redirect('/login/')

        # Perform actions based on the posted data
        # Assuming buttons in the admin_home.html have the name attribute set to these values
        if 'account_management' in request.POST:
            return redirect('/home/manageaccount')
        elif 'course_management' in request.POST:
            return redirect('/home/managecourse')
        elif 'section_management' in request.POST:
            return redirect('/home/managesection')
        elif 'logout' in request.POST:
            logout(request) # somehow log out (maybe reset section)
            return redirect('/login/')  # Redirect to login page after logout
        else:
            # If the action is unrecognized, return to the home page with an error message
            return render(request, 'admin_home.html', {'error': 'Unrecognized action'})


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
        except:
            # WE DON'T HAVE ERROR URL OR ERROR HTML ATM.
            # NEED A WAY TO RETURN AN INFORMATIVE MESSAGE FROM THE CREATESECTION METHOD
            return render(request, "error.html", {"message": message})


class DeleteSection(View):

    def get(self, request):
        return render(request, "sectionManagement/delete_section.html")


class EditSection(View):

    def get(self, request):
        return render(request, "sectionManagement/edit_section.html")


class AddTAToSection(View):

    def get(self, request):
        return render(request, "sectionManagement/add_ta_to_section.html")
