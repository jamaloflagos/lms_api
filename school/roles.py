from rest_framework_roles.roles import is_user, is_anon, is_admin


# def is_school_admin(request, view):
#     return is_user(request, view) and request.user.role == 'admin'

def is_student(request, view):
    return is_user(request, view) and request.user.role == 'student'

def is_teacher(request, view):
    return is_user(request, view) and request.user.role == 'teacher'

def is_applicant(request, view):
    return is_user(request, view) and request.user.role == 'applicant'


ROLES = {
    'user': is_user,
    'anon': is_anon,
    'admin': is_admin,
    'applicant': is_applicant,
    'student': is_student,
    'teacher': is_teacher,
}