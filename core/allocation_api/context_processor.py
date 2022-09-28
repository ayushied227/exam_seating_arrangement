from .models import Admin, Staff, Student, User


def user(request):
    try:
        user = User.objects.get(username=request.user)
        if user:
            try:
                usertype = Admin.objects.get(user=user)
            except Admin.DoesNotExist:
                usertype = Student.objects.get(user=user)
            except Student.DoesNotExist:
                usertype = Staff.objects.get(user=user)
            return {
                'usertype': usertype,
            }
    except User.DoesNotExist:
        return {'usertype': False}