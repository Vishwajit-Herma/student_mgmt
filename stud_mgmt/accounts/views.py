from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from students.models import Student
from courses.models import Course

@login_required
def dashboard(request):
    user = request.user
    role = user.profile.role
    context = {}

    if role == "ADMIN":
        context["total_students"] = Student.objects.count()
        context["total_courses"] = Course.objects.count()
        template = "accounts/dashboard_admin.html"

    elif role == "TEACHER":
        context["courses"] = Course.objects.filter(teacher=user)
        context["students"] = Student.objects.filter(course__teacher=user)
        template = "accounts/dashboard_teacher.html"

    else:  # STUDENT
        context["student"] = Student.objects.get(user=user)
        template = "accounts/dashboard_student.html"

    return render(request, template, context)
