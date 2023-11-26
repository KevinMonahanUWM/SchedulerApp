from django.shortcuts import render
from django.views import View


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
