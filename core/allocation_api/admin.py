
from django.contrib import admin
from .models import Staff, Admin, StudentBulkUpload, Venue, Student, ScheduleExamination, StudentSchedule

# Register your models here.

admin.site.register(Student)
admin.site.register(Venue)
admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(StudentBulkUpload)
admin.site.register(StudentSchedule)
admin.site.register(ScheduleExamination)