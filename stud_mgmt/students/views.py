from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Student
from .forms import StudentForm
from accounts.utils import role_required


@login_required
@role_required("ADMIN", "TEACHER")
def student_list(request):

    user = request.user
    role = user.profile.role

    if role == "ADMIN":
        students = Student.objects.select_related("user", "course")

    elif role == "TEACHER":
        students = Student.objects.select_related(
            "user", "course"
        ).filter(course__teacher=user)

    return render(request, "students/student_list.html", {
        "students": students
    })


@login_required
@role_required("ADMIN")
def student_create(request):
    form = StudentForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Student added successfully")
        return redirect("students:list")

    return render(request, "students/student_form.html", {
        "form": form
    })

@login_required
@role_required("ADMIN", "TEACHER")
def student_detail(request, pk):

    user = request.user
    role = user.profile.role

    if role == "ADMIN":
        student = get_object_or_404(Student, pk=pk)

    else:  # TEACHER
        student = get_object_or_404(
            Student,
            pk=pk,
            course__teacher=user
        )

    return render(request, "students/student_detail.html", {
        "student": student
    })

@login_required
@role_required("ADMIN")
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)

    if form.is_valid():
        form.save()
        messages.success(request, "Student updated successfully")
        return redirect("students:list")

    return render(request, "students/student_form.html", {
        "form": form
    })

@login_required
@role_required("ADMIN")
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully")
        return redirect("students:list")

    return render(request, "students/student_confirm_delete.html", {
        "student": student
    })
