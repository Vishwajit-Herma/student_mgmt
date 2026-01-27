from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course
from .forms import CourseForm
from accounts.utils import role_required

@login_required
@role_required("ADMIN", "TEACHER")
def course_list(request):
    user = request.user
    role = user.profile.role

    if role == "ADMIN":
        courses = Course.objects.select_related("teacher")
    else:  # TEACHER
        courses = Course.objects.filter(teacher=user)

    return render(request, "courses/course_list.html", {
        "courses": courses
    })

@login_required
@role_required("ADMIN")
def course_create(request):
    form = CourseForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Course created successfully")
        return redirect("courses:list")

    return render(request, "courses/course_form.html", {
        "form": form
    })

@login_required
@role_required("ADMIN", "TEACHER")
def course_update(request, pk):
    user = request.user
    role = user.profile.role

    if role == "ADMIN":
        course = get_object_or_404(Course, pk=pk)
    else:  # TEACHER
        course = get_object_or_404(Course, pk=pk, teacher=user)

    form = CourseForm(request.POST or None, instance=course)

    if form.is_valid():
        form.save()
        messages.success(request, "Course updated successfully")
        return redirect("courses:list")

    return render(request, "courses/course_form.html", {
        "form": form
    })

@login_required
@role_required("ADMIN")
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully")
        return redirect("courses:list")

    return render(request, "courses/course_confirm_delete.html", {
        "course": course
    })
