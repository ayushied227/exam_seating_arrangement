from django.urls import path, re_path

from .views import (
    allusers,
    delete_student_group, 
    index,
    remove_venue_schedule_exam, 
    staff_login, 
    admin_login_, 
    admin_dashboard, 
    student, 
    venue, 
    venue_delete, 
    staff, 
    view_student_group,
    activate,
    deactivate,
    schedule,
    detail_schedule_exam,
    student_login,
    allocate_seat,
)
from django.contrib.auth.views import LogoutView, PasswordChangeView


urlpatterns = [
    path('', index, name="index"), 
    path('login/', admin_login_, name="login"),
    path('student/login/', student_login, name="student_login"),
    path('staff/login/', staff_login, name="staff-login"),
    path('a/student/', student, name="student"),
    path('a/venue/', venue, name="venue"),
    path('a/staff/', staff, name="staff"),
    path('a/schedule/', schedule, name="schedule"),
    path('a/venue/<int:no>/', venue_delete, name="delete-venue"),
    re_path('a/activate/(?P<id>[0-9]+)(?P<path>.*)$', activate, name="activate"),
    re_path('a/deactivate/(?P<id>[0-9]+)(?P<path>.*)$', deactivate, name="deactivate"),
    re_path('a/allocate/seat/(?P<schedule_id>[0-9]+)/(?P<path>.*)$', allocate_seat, name="allocate_seat"),
    re_path('a/remove/venue/(?P<schedule_id>[0-9]+)/(?P<venue_id>[0-9]+)(?P<path>.*)$', remove_venue_schedule_exam, name="remove_venue_schedule_exam"),
    path('a/view/detail/schedule/<int:id>/', detail_schedule_exam, name="detail_schedule_exam"),
    path('a/view/student/group/<int:id>/', view_student_group, name="view_student_group"),
    path('a/delete/student/group/<int:id>/', delete_student_group, name="delete_student_group"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('a/dashboard/', admin_dashboard, name="admin-dashboard"),
    path('a/all/users/', allusers, name="all_users"),
    path('password/change/', PasswordChangeView.as_view(
         template_name='password_change_form.html',
        success_url = '/a/dashboard/'
        ), 
        name="change_password"),
]