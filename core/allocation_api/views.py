from django import contrib
from django.contrib.auth.models import User
from django.db import models
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import AdminLoginForm, ScheduleExaminationForm, StaffForm
from .models import ScheduleExamination, Student, Admin, Staff, StudentBulkUpload, StudentSchedule
from django.contrib.auth import authenticate, login, logout
from .forms import VenueForm, StudentBulkUploadForm, AddVenueForm
from .models import Venue
from django.contrib import messages
import os
from .utility import save_new_students_from_csv, delete_students_from_csv, schedule_students_to_exam
from core.settings import BASE_DIR
import logging
# Create your views here.

def index(request):
    return render(request, 'index.html')


def admin_login_(request):
    form = AdminLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["admin_id"]
        password = form.cleaned_data['password']
        try:
            user = Admin.objects.get(user__username=username)
            if user.user.is_active:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return redirect("admin-dashboard")
                else:
                    messages.success(
                        request, 'Administator / Secret Login does not match')
            else:
                messages.success(
                    request, 'Authorisation Error Contact Admin To Regain Access')
        except Exception as e:
            messages.success(
                request, 'Administator / Secret Login does not match'.format(e))
    context = {
        'form': form
    }
    return render(request, "login.html", context)
    

def staff_login(request):
    form = AdminLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["admin_id"]
        password = form.cleaned_data['password']
        try:
            user = Staff.objects.get(user__username=username)
            if user.user.is_active:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return redirect("admin-dashboard")
                else:
                    messages.success(
                        request, 'Staff ID/ Password does not match')
            else:
                messages.success(
                    request, 'Authorisation Error Contact Admin To Regain Access')
        except Exception as e:
            messages.success(
                request, 'Staff ID/ Password does not match'.format(e))
    context = {
        'form': form
    }
    return render(request, "staff-login.html", context)

def student_login(request):
    form = AdminLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["admin_id"]
        password = form.cleaned_data['password']
        try:
            user = Student.objects.get(user__username=username)
            if user.user.is_active:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return redirect("student-dashboard")
                else:
                    messages.success(
                        request, 'Registration Number/ Date Of Birth Does Not March')
            else:
                messages.success(
                    request, 'Authorisation Error Contact Admin To Regain Access')
        except Exception as e:
            messages.success(
                request, 'Registration Number/ Date Of Birth Does Not March'.format(e))
    context = {
        'form': form,
        'student': 1,
    }
    return render(request, "staff-login.html", context)

def admin_dashboard(request):
    return render(request, "admin-dahboard.html")


def staff(request):
    form = StaffForm(request.POST, None)
    if form.is_valid():
        print (1)
        full_name = form.cleaned_data['full_name']
        staff_id = form.cleaned_data['staff_id']
        user = User()
        user.first_name = full_name
        user.username = staff_id
        user.set_password('123456')
        user.save()
        Staff.objects.create(
            user=user,
            staff_id=staff_id
        ) 
        messages.success(request, "User Sucessfully created with the default password 123456")
        
        return redirect('staff')
    context = {
        "form": form,
        'staffs': Staff.objects.all()
    }
    return render(request, "staff.html", context)


def venue(request):
    form = VenueForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Venue Sucessfully Added")

    context ={
        'venues': Venue.objects.filter(show=True),
        'form': form
    }
    return render(request, "venue.html", context)

def venue_delete(request, no):
    venue = Venue.objects.get(id=no)
    venue.show = False
    venue.save()
    return redirect('venue')


def student(request):
    form = StudentBulkUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            csv_file = form.cleaned_data['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('student')
            # If file is too large
            if csv_file.multiple_chunks():
                messages.error(request, 'Uploaded file is too big (%.2f MB)' %(csv_file.size(1000*1000),))
                return redirect('student')

            # save and upload file 
            instance = StudentBulkUpload.objects.create(
                session=form.cleaned_data['session'],
                csv_file=form.cleaned_data['csv_file']
            )
            # get the path of the file saved in the server
            file_path = os.path.join(BASE_DIR, instance.csv_file.path)
            print (file_path)

            # a function to read the file contents and save the student details
            total_student = save_new_students_from_csv(file_path, request, instance)
            instance.total_students = total_student
            instance.save()
            # do try catch if necessary
        except Exception as e:
            logging.getLogger('error_logger').error('Unable to upload file. ' + repr(e))
            messages.error(request, 'Unable to upload file. ' + repr(e))
    context = {
        'studentSET': StudentBulkUpload.objects.all(),
        'form': form 
    }
    return render(request, "student.html", context)


def delete_student_group(request, id):
    student_group = get_object_or_404(StudentBulkUpload, id=id)
    path = student_group.csv_file.path
    print (path)
    delete_students_from_csv(path, request)
    student_group.delete()
    return redirect('student')


def view_student_group(request, id):
    student_group = get_object_or_404(StudentBulkUpload, id=id)
    students = Student.objects.filter(group=student_group)
    context = {
        "student_group": student_group,
        "students": students
    }
    return render(request, 'students_details.html', context)


def activate(request, id, path):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect(path)


def deactivate(request, id, path):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    print(user)
    return redirect(path)


def schedule(request):
    form = ScheduleExaminationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            csv_file = form.cleaned_data['student_record']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('schedule')
            # If file is too large
            if csv_file.multiple_chunks():
                messages.error(request, 'Uploaded file is too big (%.2f MB)' %(csv_file.size(1000*1000),))
                return redirect('schedule')

            # save and upload file 
            instance = ScheduleExamination.objects.create(
                student_record=csv_file,
                duration=form.cleaned_data['duration'],
                exam_date=form.cleaned_data['exam_date'],
                name=form.cleaned_data['name']
            ) 
            # get the path of the file saved in the server
            file_path = os.path.join(BASE_DIR, instance.student_record.path)
            
            # a function to read the file contents and save the student details
            total_student = schedule_students_to_exam(file_path, request, instance)
            instance.total_student = total_student
            instance.save()
            
            # do try catch if necessary
        except Exception as e:
            logging.getLogger('error_logger').error('Unable to upload file. ' + repr(e))
            messages.error(request, 'Unable to upload file. ' + repr(e))
    
    context = {
        "form": form,
        "schedule_examination": ScheduleExamination.objects.all()
    }
    return render(request, "schedule_examination.html", context)


def detail_schedule_exam(request, id):
    form = AddVenueForm(request.POST or None)
    scheduled_exam = ScheduleExamination.objects.get(id=id)
    students = StudentSchedule.objects.filter(scheduled_exam=scheduled_exam)
    if form.is_valid():
        venue = form.cleaned_data['venue']
        if scheduled_exam.total_student > scheduled_exam.current_capacity:
            scheduled_exam.venue.add(venue)
            scheduled_exam.current_capacity = scheduled_exam.current_capacity + venue.capacity
            scheduled_exam.save()
            venue.availability = False
            venue.save()
            messages.success(request, "Venue add to exam")
            return redirect('detail_schedule_exam', id=id)
        

    context = {
        'form': form,
        'scheduled_exam': scheduled_exam,
        "students": students
    }
    return render(request, 'detail_schedule_exam.html', context)


def remove_venue_schedule_exam(request, venue_id, schedule_id, path):
    venue = Venue.objects.get(id=venue_id)
    scheduled_exam = ScheduleExamination.objects.get(id=schedule_id)
    scheduled_exam.venue.remove(venue)
    scheduled_exam.current_capacity = scheduled_exam.current_capacity - venue.capacity
    scheduled_exam.save()
    venue.availability = True
    venue.save()
    messages.success(request, "Venue removed form scheduled exam")
    return redirect(path)
        


def allocate_seat(request, schedule_id, path):
    scheduled_exam = ScheduleExamination.objects.get(id=schedule_id)
    if scheduled_exam.current_capacity < scheduled_exam.total_student:
        messages.error(request,"Venue can not fit student, Kindly add more venues")
        return redirect(path)
    


def allusers(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, "allusers.html", context)