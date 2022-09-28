from .models import Student, StudentSchedule
from django.contrib.auth.models import User
from django.contrib import messages
import csv
from django.db import IntegrityError



def save_new_students_from_csv(file_path, request, group):
    # do try catch accordingly
    # open csv file, read lines
    with open(file_path, 'r') as fp:
        students = csv.reader(fp, delimiter=',')
        row = 0
        total_student = 0
        for student in students:
            if row==0:
                headers = student
                row = row + 1
            else:
                # create a dictionary of student details
                new_student_details = {}
                for i in range(len(headers)):
                    new_student_details[headers[i]] = student[i]
                    print (new_student_details)
                # for the foreign key field current_class in Student you should get the object first and reassign the value to the key
                try:                    
                    user = User()
                    user.first_name = new_student_details['first_name'] + " " +  new_student_details['middle_name'] + " " + new_student_details['last_name']
                    user.set_password(new_student_details['dob'])
                    user.username = new_student_details['reg_no']
                    user.save()
                    Student.objects.create(
                        user=user,
                        registration_number=user.username,
                        group=group
                    )
                    total_student = total_student + 1
                except IntegrityError:
                    messages.error(request, "Error: Student ({}) exist at SN - {}".format(new_student_details['reg_no'], new_student_details['s/n']))
                row = row + 1
        messages.success(request, "Non error field Records Uploaded Successfully")
        fp.close()
        return total_student


def delete_students_from_csv(file_path, request):
    
    with open(file_path, 'r') as fp:
        students = csv.reader(fp, delimiter=',')
        row = 0
        total_student = 0
        for student in students:
            if row==0:
                headers = student
                row = row + 1
            else:
                # create a dictionary of student details
                new_student_details = {}
                for i in range(len(headers)):
                    new_student_details[headers[i]] = student[i]
                    
                # for the foreign key field current_class in Student you should get the object first and reassign the value to the key
                try:                    
                    user = User.objects.get(username=new_student_details['reg_no'])
                    student = Student.objects.get(user=user)
                    user.delete()
                    student.delete()
                    total_student = total_student + 1
                except 404:
                    pass
                row = row + 1
        messages.success(request, "Successfully deleted Student group with {} users".format(total_student))
        fp.close()


def schedule_students_to_exam(file_path, request, scheduled_exam):
    with open(file_path, 'r') as fp:
        students = csv.reader(fp, delimiter=',')
        row = 0
        total_student = 0
        for student in students:
            if row==0:
                headers = student
                row = row + 1
            else:
                # create a dictionary of student details
                new_student_details = {}
                for i in range(len(headers)):
                    new_student_details[headers[i]] = student[i]
                    
                # for the foreign key field current_class in Student you should get the object first and reassign the value to the key
                
                try:
                    registration = int(new_student_details['reg_no'])
                    print(registration)
                    student = Student.objects.get(registration_number=registration)
                    StudentSchedule.objects.create(
                        student=student,
                        scheduled_exam=scheduled_exam,
                        seat_number=row
                    )

                    total_student = total_student + 1
                except Exception as e:
                    messages.error(request, "{}".format(e))
                row = row + 1
        messages.success(request, "Added {} Student to exam".format(row))
        fp.close()
    return total_student