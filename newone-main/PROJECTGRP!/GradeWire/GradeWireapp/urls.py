from django.urls import path
from  . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('', views.index,name='index'),
    path('tregister/teacherlogin/', LoginView.as_view(template_name='teach_login.html'),name='teacherLogin'),
    path('tregister/', views.Teacher_signup_view,name='teacherRegister'),
    path('sregister/', views.Student_signup_view,name='studentRegister'),
    path('studentlogin/', LoginView.as_view(template_name='stdnt_login.html'),name='studentlogin'),
    path('student-dashboard/', views.student_dashboard_view,name='studentDashboard'),
    path('teach-dashboard/', views.teacher_dashboard_view,name='teacherDashboard'),
    
]
