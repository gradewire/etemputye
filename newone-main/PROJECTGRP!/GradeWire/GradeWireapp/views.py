from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group
from . import forms, models

# Create your views here.

def index(request):
    return render(request, 'index.html')

def teacherLogin(request):
    if request.method == 'POST':
        username = request.POST.get('teacher_id')
        password = request.POST.get('password')

        # Authenticate the teacher using saved username and password
        teacher = authenticate(request, username=username, password=password)

        if teacher is not None:
            login(request, teacher)
            # Redirect to the teacher's dashboard after successful login
            return redirect('teacher_dashboard')  # Replace with actual teacher dashboard URL
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('teacherlogin')  # Redirect back to login page if authentication fails

    return render(request, 'teach_login.html')
def student_dashboard_view(request):
    return render(request, 'stdnt_dashboard.html')

def teacher_dashboard_view(request):
    return render(request, 'teach_dashboard.html')

def studentLogin(request):
    return render(request, 'stdnt_login.html')

def Teacher_signup_view(request):
    teacherForm = forms.TeacherForm()
    mydict = {'teacherForm': teacherForm}

    if request.method == 'POST':
        teacherForm = forms.TeacherForm(request.POST, request.FILES)

        if teacherForm.is_valid():
            # Create the user from the form
            username = teacherForm.cleaned_data['username']
            password = teacherForm.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)  # Create a user with hashed password

            # Save other teacher details (e.g., name, email) to the Teacher model
            teacher = teacherForm.save(commit=False)  # Don't save yet to add the user to it
            teacher.user = user
            teacher.save()

            # Add user to the "TEACHER" group
            teacher_group, created = Group.objects.get_or_create(name='TEACHER')
            user.groups.add(teacher_group)

            # Redirect to the login page
            return HttpResponseRedirect('teacherlogin')

    return render(request, 'teach_register.html', context=mydict)

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

from .forms import StudentForm
def Student_signup_view(request):
    if request.method == 'POST':
        studentForm = StudentForm(request.POST, request.FILES)

        if studentForm.is_valid():
            # Create user with username and password
            username = studentForm.cleaned_data['username']
            password = studentForm.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)  # Create a user with hashed password

            # Save other student details (e.g., name, email) to the Student model
            student = studentForm.save(commit=False)  # Don't save yet to add the user to it
            student.user = user
            student.save()

            # Add user to the "STUDENT" group
            student_group, created = Group.objects.get_or_create(name='STUDENT')
            user.groups.add(student_group)

            return redirect('studentlogin')  # Redirect to student login page

    else:
        studentForm = StudentForm()

    return render(request, 'stdnt_register.html', {'studentForm': studentForm})

def afterlogin_view(request):
    if is_teacher(request.user):
        accountapproval = models.Teacher.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('admin-dashboard')  # Adjust with the correct URL
        else:
            # Teacher waiting for approval could be redirected to another page
            return redirect('teacher-dashboard')  # Adjust accordingly
        
    elif is_student(request.user):
        return redirect('student-home')  # Adjust to the actual student home page URL
    else:
        return redirect('teacher-home')  # Adjust to the actual teacher home page URL
