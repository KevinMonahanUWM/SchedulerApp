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
        return render(request, "course_management.html")


class CreateCourse(View):

    def get(self, request):
        return render(request, "create_course.html")


class DeleteCourse(View):

    def get(self, request):
        return render(request, "delete_course.html")


class EditCourse(View):

    def get(self, request):
        return render(request, "edit_course.html")


class AddInstructorToCourse(View):

    def get(self, request):
        return render(request, "add_instructor_to_course.html")
