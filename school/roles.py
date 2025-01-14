from rest_framework_roles.roles import is_user, is_anon, is_admin


# def is_school_admin(request, view):
#     return is_user(request, view) and request.user.role == 'admin'

def is_student(request, view):
    return is_user(request, view) and request.user.role == 'Student'

def is_teacher(request, view):
    return is_user(request, view) and request.user.role == 'Teacher'

def is_applicant(request, view):
    return is_user(request, view) and request.user.role == 'Applicant'

def is_librarian(request, view):
    return is_user(request, view) and request.user.role == 'Librarian'


ROLES = {
    'user': is_user,
    'anon': is_anon,
    'admin': is_admin,
    'applicant': is_applicant,
    'librarian': is_librarian,
    'student': is_student,
    'teacher': is_teacher,
}