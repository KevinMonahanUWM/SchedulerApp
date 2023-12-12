"""
URL configuration for SchedulerWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from TAScheduler.views import Home, CourseManagement, CreateCourse, EditCourse, UserAssignments, \
    Login, AccountManagement, CreateAccount, EditAccount, SectionManagement, CreateSection, EditSection, \
    AddUserToSection, DeleteSection, Error, Success, Forgot_Password, ChooseSectionForUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Login.as_view()),
    path('home/', Home.as_view()),
    path('home/managecourse/', CourseManagement.as_view()),
    path('home/managecourse/create/', CreateCourse.as_view()),
    path('home/managecourse/edit/', EditCourse.as_view()),
    path('home/managecourse/assignuser/', UserAssignments.as_view()),
    path('home/manageaccount/', AccountManagement.as_view()),
    path('home/manageaccount/create/', CreateAccount.as_view()),
    path('home/manageaccount/edit/', EditAccount.as_view()),
    path('home/managesection/', SectionManagement.as_view()),
    path('home/managesection/create/', CreateSection.as_view()),
    path('home/managesection/delete/', DeleteSection.as_view()),
    path('home/managesection/edit/', EditSection.as_view()),
    path('home/managesection/adduser/', AddUserToSection.as_view()),
    path('home/managesection/adduser/choosesection/', ChooseSectionForUser.as_view()),
    path('home/error/', Error.as_view()),
    path('home/success/', Success.as_view()),
    path('forgot_password/', Forgot_Password.as_view())
]

urlpatterns += staticfiles_urlpatterns()
