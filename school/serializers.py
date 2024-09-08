from rest_framework import serializers
from .models import (
    Class,
    Student,
    Teacher,
    Parent,
    Lesson,
    Score,
    Grade,
    Book,
    BookPurchase,
    BookSale,
    Checkout,
    Attendance,
    Applicant, 
    EntranceExamQuestion, 
    EntranceExamScore,
    Course,
    Module,
    Assignment, 
    Exam,
    ClassSchedule
)

class ExamSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = '__all__'

    def get_course(self, obj):
        return f"{obj.course.title}"
    
class ClassScheduleSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = ClassSchedule
        fields = '__all__'

    def get_course(self, obj):
        return f"{obj.course.title}"

class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'

    def get_course(self, obj):
        return f"{obj.lesson.module.course.title}"

class EntranceExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceExamQuestion
        fields = '__all__'

class EntranceExamScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceExamScore
        fields = '__all__'

class ApplicantSerializer(serializers.ModelSerializer):
    class_applied_for = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())

    class Meta:
        model = Applicant
        fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
    # form_teacher_details = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = "__all__"

    # def get_form_teacher_details(self, obj):
    #     try:
    #         return {
    #             "name": f"{obj.form_teacher.first_name} {obj.form_teacher.last_name}"
    #         }
    #     except Class.form_teacher.RelatedObjectDoesNotExist:
    #         return {"name": "No form teacher assigned"}


class StudentSerializer(serializers.ModelSerializer):
    _class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), write_only=True)
    class_details = serializers.SerializerMethodField()
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = "__all__"
    
    def get_class_details(self, obj): 
        return {
            "id": obj._class.id,
            "name": obj._class.name
        }

class TeacherSerializer(serializers.ModelSerializer):
    _class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all(), write_only=True)
    form_class_details = serializers.SerializerMethodField()
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'
    
    def get_form_class_details(self, obj): 
        return {
            "id": obj._class.id,
            "name": obj._class.name
        }


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    # _class = serializers.CharField(write_only=True)
    # class_details = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = "__all__"
    
    # def get_class_details(self, obj):
    #     return {
    #         "id": obj._class.id,
    #         "name": obj._class.name
    #     }


class ScoreSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), write_only=True)
    lesson_topic = serializers.CharField(source='lesson.topic', read_only=True)
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True)
    student_details = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = "__all__"
    
    def get_student_details(self, obj):
        return {
            "name": f"{obj.student.first_name} {obj.student.last_name}"
        }
    


class GradeSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source='subject.name', read_only=True)
    student = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ["subject", "student", "value"]

    def get_student(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), write_only=True)
    student_details = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = '__all__'

    def get_student_details(self, obj):
         # Handle case where obj is a dict (e.g., during create)
        if isinstance(obj, dict):
            student_id = obj.get('student')
            student = Student.objects.get(id=student_id)
            return {
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}"
            }
        # Handle case where obj is an instance of Attendance
        return {
            "id": obj.student.id,
            "name": f"{obj.student.first_name} {obj.student.last_name}"
        }


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "copies", "location"]


class BookPurchaseSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = BookPurchase
        fields = [
            "book",
            "date_purchased",
            "quantity",
            "unit_price",
            "total_price",
            "supplier",
        ]


class BookSaleSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = BookSale
        fields = [
            "book",
            "date_sold",
            "quantity",
            "unit_price",
            "total_price",
            "student",
        ]


class CheckoutSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    book = serializers.CharField(source="book.title", read_only=True)

    class Meta:
        model = Checkout
        fields = ["book", "date_checked_out", "student", "days_requested"]

    def get_student(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    
class CourseSerializer(serializers.ModelSerializer):
    # modules_count = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = '__all__'
    
    # def get_modules_count(self, obj):
    #     return f"{obj.modules.all().count()}"

class Moduleserializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
