from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from school.models import Student, Teacher, Applicant, TuitionFee, Term

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        current_date = ''
        current_term = Term.objects.filter(end_date__gt=current_date).first()
        token['role'] = user.role
        token['username'] = user.username
        
        if user.role == 'Student':
            email = user.email
            student = Student.objects.filter(email=email).first()
            tuition_fee = TuitionFee.objects.filter(student=student).first()
            class_id = student._class.id
            token['class_id'] = class_id
            token['has_made_full_tuition_fee_payment'] = tuition_fee.has_made_full_payment
            token['term_id'] = current_term.id
        elif user.role == 'Teacher':
            email = user.email
            teacher = Teacher.objects.filter(email=email).first()
            token['term_id'] = current_term.id
            if teacher.is_form_teacher:
                class_id = teacher._class.id
                token['class_id'] = class_id
                token['is_form_teacher'] = True
        elif user.role == 'Applicant':
            email = user.email
            applicant = Applicant.objects.filter(email=email).first()
            token['has_made_payment'] = applicant.has_made_payment

        
        return token



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        access_token = response.data.get('access')

        if refresh_token:
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,  # Set to False if you're testing locally
                samesite='Lax',  # Can be 'Strict' or 'None' depending on your requirements
                max_age=7 * 24 * 60 * 60,  # 7 days
            )
            del response.data['refresh']  # Remove refresh token from response body
        
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token is missing."}, status=status.HTTP_400_BAD_REQUEST)

        request.data['refresh'] = refresh_token
        response = super().post(request, *args, **kwargs)
        
        return response
