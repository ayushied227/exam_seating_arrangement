from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    session = models.CharField(max_length=500)
    csv_file = models.FileField(upload_to='')
    total_students = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.id

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=500)
    group = models.ForeignKey(StudentBulkUpload, on_delete=models.CASCADE)

    def __str__(self):
        return "{}.".format(self.user.username)


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=500)
    
    def __str__(self):
        return "{}.".format(self.user.username)


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin_id = models.CharField(max_length=500)
    
    def __str__(self):
        return "{}.".format(self.user.username)


class Venue(models.Model):
    name = models.CharField(max_length=500)
    address = models.TextField()
    capacity = models.IntegerField(default=0)
    availability = models.BooleanField(default=True)
    until = models.TimeField(blank=True, null=True)
    show = models.BooleanField(default=True)

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.capacity)


class ScheduleExamination(models.Model):
    name = models.CharField(max_length=500)
    exam_date = models.DateField()
    duration = models.IntegerField()
    student_record = models.FileField(upload_to='exam/')
    venue = models.ManyToManyField(Venue, blank=True)
    total_student = models.IntegerField(default=0)
    current_capacity = models.IntegerField(default=0)

class StudentSchedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    scheduled_exam = models.ForeignKey(ScheduleExamination, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, null=True)