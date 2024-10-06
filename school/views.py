import random
import string
from django.http import Http404, HttpResponseBadRequest
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



from .models import *
from .serializers import *


class ClassCourseList(generics.ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def get_queryset(self):
        class_id = self.request.GET.get('class_id')
        _class = Class.objects.get(id=class_id)
        queryset = _class.courses.all()
        
        return queryset
    
class ClassStudentList(generics.ListAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def get_queryset(self):
        class_id = self.request.GET.get('class_id')
        _class = Class.objects.get(id=class_id)
        queryset = _class.students.all()
        
        return queryset
class EntranceExamQuestionList(generics.ListCreateAPIView):
    queryset = EntranceExamQuestion.objects.all()
    serializer_class = EntranceExamQuestionSerializer

class EntranceExamScoreList(generics.ListCreateAPIView):
    queryset = EntranceExamScore.objects.all()
    serializer_class = EntranceExamScoreSerializer

class EntranceExamScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntranceExamScore.objects.all()
    serializer_class = EntranceExamScoreSerializer

    def get_object(self):
        queryset = self.get_queryset()
        applicant_id = self.kwargs.get('applicant_id')
        print(applicant_id)

        obj = generics.get_object_or_404(queryset, applicant_id=applicant_id)
        return obj

class QuestionList(generics.ListCreateAPIView):
    queryset = EntranceExamQuestion.objects.all()
    serializer_class = EntranceExamQuestionSerializer

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntranceExamQuestion.objects.all()
    serializer_class = EntranceExamQuestionSerializer

#  applicant views
class ApplicantList(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    def perform_create(self, serializer):
        contact_mail = serializer.validated_data.get('contact_mail')

        # Check if there is an existing applicant with the same contact_mail or parent_contact_mail
        if Applicant.objects.filter(contact_mail=contact_mail).exists():
            response_message = {"contact_mail": "Email already exists"}
            return HttpResponseBadRequest(response_message)

        applicant = serializer.save()
        # Send email notification after saving the applicant
        self.send_email(applicant)

    def send_email(self, applicant):
        subject = 'New Applicant Created'
        message = f'''
        You have successfully submitted your application, proceed to take your entrance exam with the link beloe

        Link: http://localhost:3000/entrance-exam/{applicant.application_id} 
        '''
        recipient_list = [applicant.contact_mail]  # Or any email you want to notify
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

class ApplicantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

class StudyGroupList(generics.ListCreateAPIView):
    """
        This view
            creates a new study group
            lists all study groups
    """
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer

# Class Views
# @method_decorator(csrf_exempt, name='dispatch')
class ClassList(generics.ListCreateAPIView):
    """
        This view
          creates a new class
          get all classes
          get all students of a class
          get all courses offered by a class
          get all modules of each course offered by a class
          get all lessons of each modules of each courses offered by a class
          get all assignmnets of a class
          get all exams of a class
    """

    def get_serializer_class(self):

        data_type = self.kwargs.get('data_type')
        
        if self.request.method == 'GET':
            if data_type == 'students':
                return StudentSerializer  
            elif data_type == 'courses':
                return CourseSerializer 
            elif data_type == 'modules':
                return Moduleserializer
            elif data_type == 'lessons':
                return LessonSerializer
            elif data_type == 'assignments':
                return UnitTestSerializer
            elif data_type == 'exams':
                return ExamSerializer
            elif data_type == 'clas-schedules':
                return ClassScheduleSerializer
            else:
                return ClassSerializer
        return ClassSerializer  

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')

        if class_id:
            _class = Class.objects.get(pk=class_id)
            data_type = self.kwargs.get('data_type')
            course_id = self.kwargs.get('course_id')
            module_id = self.kwargs.get('module_id')

            if data_type == 'students':
                return _class.students.all()
            elif data_type == 'courses':
                return _class.courses.all()
            elif data_type == 'modules':
                course = _class.courses.get(pk=course_id)
                modules = course.modules.all()
                return modules
            elif data_type == 'lessons':
                course = _class.courses.get(pk=course_id)
                module = course.modules.get(pk=module_id)
                lessons = module.lessons.all()
                return lessons
            elif data_type == 'tests':
            # Get all lessons across all courses and modules for the class
                # lessons = Lesson.objects.filter(module__course___class=class_id)
            # Get all assignments related to those lessons
                return UnitTest.objects.filter(module__course___class=class_id)
            elif data_type == 'exams':
                exams = Exam.objects.filter(course___class=class_id)
                return exams
            elif data_type == 'class-schedules':
                exams = ClassSchedule.objects.filter(course___class=class_id)
                return exams
            else:
                return Http404("Invalid URL segment. Use 'courses' or 'students'.")

        return Class.objects.all()


class ClassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

# Student Views
class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentInfoList(generics.ListAPIView):
    """
        This view
            creates a new student
            lists all of the scores obtained by a student
            lists all groups related to a student
    """

    def get_serializer_class(self):
        data_type = self.kwargs.get('data_type')

        if data_type == 'scores':
            return ScoreSerializer
        else:
            return StudyGroupSerializer
    
    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        data_type = self.kwargs.get('data_type')
        status = self.request.GET.get('status')

        if data_type == 'scores':
            return Score.objects.filter(student=student_id)
        elif data_type == 'groups':
            student = get_object_or_404(Student, pk=student_id)

            if status == 'member':
                # student = get_object_or_404(Student, pk=student_id)
                return student.study_groups.all()
            elif status == 'non-member':
                # Groups created by other students in the same class
                    class_members = student._class.students.exclude(id=student.id)
                    other_classmate_groups = StudyGroup.objects.filter(
                        creator__in=class_members
                    ).exclude(
                        Q(students=student) | Q(creator=student)
                    )

                    return other_classmate_groups

        else:
            return Student.objects.all()

class StudyGroupInfoList(generics.ListAPIView):
    """
        This view
            lists all members of a group
            lists all messages of a group
    """

    def get_serializer_class(self):
        data_type = self.kwargs.get('data_type')

        if data_type == 'messages':
            return MessageSerializer
        elif data_type == 'members':
            return StudentSerializer

    def get_queryset(self):
        data_type = self.kwargs.get('data_type')
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(StudyGroup, pk=group_id)

        if data_type == 'messages':
            return group.messages.all()
        elif data_type == 'members':
            return group.students.all()

class StudyGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    """
        This view 
            adds a new member to a group
    """

    def perform_update(self, serializer):
        student_id = self.kwargs['student_id']
        group_id = self.kwargs['pk']
        group = get_object_or_404(StudyGroup, pk=group_id)
        student = get_object_or_404(Student, pk=student_id)
        group.students.add(student)

        serializer.save()


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# Teacher Views
class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def perform_create(self, serializer):
        # Generate a random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
        # Save the teacher instance
        teacher = serializer.save(password=password)


        # Send an email to the teacher with the password
        send_mail(
            subject='Your Account Has Been Created',
            message=f'''
            Dear {teacher.first_name},

            Your account has been created. Below are your login credentials:

            Email: {teacher.email}
            Password: {password}

            Please log in and change your password as soon as possible.

            Best regards,
            The School Management Team
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[teacher.email]
        )


class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


# Parent Views
class ParentList(generics.ListCreateAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer


class ParentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer


# Lesson Views
class LessonList(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        _class = serializer.validated_data.get('_class')
        class_instance = Class.objects.get(name=_class)
        serializer.save(_class=class_instance)

    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.request.GET.get('class_id')
        subject = self.request.GET.get('subject')
        teacher_id = self.request.GET.get('teacher_id')

        if class_id and subject:
            queryset = queryset.filter(_class=class_id, subject=subject)

        elif teacher_id and subject:
            queryset = queryset.filter(teacher=teacher_id, subject=subject)
        
        return queryset

class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


# Score Views
class ScoreList(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        print(self.request.data)
        
        queryset = super().get_queryset()
        student_id = self.request.GET.get('student_id')
        subject = self.request.GET.get('subject_id')
        score_type = self.request.GET.get('score_type')
        student_own = self.request.GET.get('student_own')

        if score_type and score_type == 'Quiz' and student_id and subject:
            # filter scores that are quiz for a student in a subject
            queryset = queryset.filter(student=student_id, subject=subject, type=score_type)
        
        elif score_type and score_type == 'Exam' and subject and not student_own:
            # filter the exam scores of a subject
            queryset = queryset.filter(type=score_type, subject=subject)

        elif score_type and score_type == 'Exam' and student_own and student_id:
            # filter exam scores for a student
            queryset = queryset.filter(type=score_type, student=student_id)

        return queryset

class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    
    def get_object(self):
        queryset = self.get_queryset()
        student_id = self.request.GET.get('student_id')
        lesson_id = self.request.GET.get('lesson_id')
        subject = self.request.GET.get('subject')
        score_type = self.request.GET.get('score_type')

        if score_type == 'Quiz':
            # get a lesson quiz score for a student
            print('score get')
            obj = generics.get_object_or_404(queryset, lesson=lesson_id, student=student_id,)
            return obj
        elif score_type == 'Exam':
            # get an exam score for a student in a subject
            obj = generics.get_object_or_404(queryset, subject=subject, student=student_id)
            return obj
            # print(f"obj {obj}")
        
# Grade Views
class GradeList(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

# Attendance Views
class AttendanceList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def perform_create(self, serializer):
        student_id = serializer.validated_data.get('student')
        date_marked = serializer.validated_data.get('data_submitted')

        if Attendance.objects.filter(student=student_id, date_marked=date_marked).exists():
            return HttpResponseBadRequest({"detail": "You have already marked an attendance for this student today"})
        
        serializer.save()
        
    def get_queryset(self):
        queryset = super().get_queryset()
        student_id = self.request.GET.get('student_id')

        if student_id:
            queryset = queryset.filter(student=student_id)
        
        return queryset

class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


# Book Views
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Book Purchase Views
class BookPurchaseList(generics.ListCreateAPIView):
    queryset = BookPurchase.objects.all()
    serializer_class = BookPurchaseSerializer


class BookPurchaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookPurchase.objects.all()
    serializer_class = BookPurchaseSerializer


# Book Sale Views
class BookSaleList(generics.ListCreateAPIView):
    queryset = BookSale.objects.all()
    serializer_class = BookSaleSerializer


class BookSaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookSale.objects.all()
    serializer_class = BookSaleSerializer


# Checkout Views
class CheckoutList(generics.ListCreateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer


class CheckoutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = JSONParser().parse(request)
        
        role = data.get('role')
        email = data.get('email')
        password = data.get('password')

        if role == 'student':
            print(email, password)
            try:
                student = Student.objects.get(email=email, password=password)
            except Student.DoesNotExist:
                raise Http404
            
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        elif role == 'teacher':
            try:
                teacher = Teacher.objects.get(email=email, password=password)
            except Teacher.DoesNotExist:
                raise Http404

            serializer = TeacherSerializer(teacher)
            return Response({'id': serializer.data['id']})

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 



class ModuleList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = Moduleserializer

class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = Moduleserializer

class PaymentList(generics.ListCreateAPIView):
    """
        This view
            creates a payment for a class
            gets all payment of a class
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        # type = self.kwargs.get('type')
        queryset = Payment.objects.filter(_class=class_id)

        return queryset
    
class StudentPaymentList(generics.ListCreateAPIView):
    """
        This view 
            gets all payments made by students in a class
    """
    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        type = self.kwargs.get('type')
        print(type)

        _class = get_object_or_404(Class, pk=class_id)
        

        students = Student.objects.filter(
            _class=_class,  # Ensure the student is in the specified class
            _class__payments__type=type  # Ensure the student has a payment of the specified type
        )

        # Now filter StudentPayment for those students
        student_payments = StudentPayment.objects.filter(
            student__in=students
        ).distinct('student')

        return student_payments
    
class StudentPaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        This view 
            retrieve, delete and update payment made by a student
    """
    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer

    def get_serializer_context(self):
        index = self.request.GET.get('index')
        context = super().get_serializer_context()
        context['action'] = self.kwargs['action']
        context['amount'] = self.request.data.get('amount')
        if index:
            context['index'] = int(index)
        return context

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)