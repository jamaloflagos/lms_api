from rest_framework import serializers
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    _class = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(), write_only=True
    )
    class_details = serializers.SerializerMethodField(source="_class")
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = "__all__"

    def get_class_details(self, obj):
        return {"id": obj._class.id, "name": obj._class.name}


class StudyGroupSerializer(serializers.ModelSerializer):
    creator_details = serializers.SerializerMethodField()
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = StudyGroup
        fields = "__all__"
        read_only_fields = ["group_name", "created_at"]

    def create(self, validated_data):
        creator = validated_data.get("creator")
        # student = Student.objects.get(id=creator)
        group = StudyGroup.objects.create(**validated_data)
        group.students.add(creator)

        return group

    def get_creator_details(self, obj):
        return {
            "id": obj.creator.id,
            "name": f"{obj.creator.first_name} {obj.creator.last_name}",
        }


class MessageSerializer(serializers.ModelSerializer):
    sender_details = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_sender_details(self, obj):
        return {
            "id": obj.sender.id,
            "name": f"{obj.sender.first_name} {obj.sender.last_name}",
        }


class ExamSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = "__all__"

    def get_course(self, obj):
        return f"{obj.course.title}"


class ClassScheduleSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = ClassSchedule
        fields = "__all__"

    def get_course(self, obj):
        return f"{obj.course.title}"


class UnitTestSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = UnitTest
        fields = "__all__"

    def get_course(self, obj):
        return f"{obj.lesson.module.course.title}"


class EntranceExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceExamQuestion
        fields = "__all__"


class EntranceExamScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceExamScore
        fields = "__all__"


class ApplicantSerializer(serializers.ModelSerializer):
    class_applied_for = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())

    class Meta:
        model = Applicant
        fields = "__all__"


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


class TeacherSerializer(serializers.ModelSerializer):
    _class = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(), write_only=True
    )
    form_class_details = serializers.SerializerMethodField()
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"

    def get_form_class_details(self, obj):
        return {"id": obj._class.id, "name": obj._class.name}


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"


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
    lesson = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(), write_only=True
    )
    lesson_topic = serializers.CharField(source="lesson.topic", read_only=True)
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), write_only=True
    )
    student_details = serializers.SerializerMethodField()

    class Meta:
        model = Score
        fields = "__all__"
        read_only_fields = ["total_obtainable_mark"]

    def get_student_details(self, obj):
        return {"name": f"{obj.student.first_name} {obj.student.last_name}"}

    def create(self, validated_data):
        return Score.objects.create(tota_obtainable_mark=sum("obtainable_mark"))


class GradeSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(source="subject.name", read_only=True)
    student = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ["subject", "student", "value"]

    def get_student(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), write_only=True
    )
    student_details = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = "__all__"

    def get_student_details(self, obj):
        # Handle case where obj is a dict (e.g., during create)
        if isinstance(obj, dict):
            student_id = obj.get("student")
            student = Student.objects.get(id=student_id)
            return {
                "id": student.id,
                "name": f"{student.first_name} {student.last_name}",
            }
        # Handle case where obj is an instance of Attendance
        return {
            "id": obj.student.id,
            "name": f"{obj.student.first_name} {obj.student.last_name}",
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
    modules_count = serializers.SerializerMethodField()
    course_status = serializers.CharField(write_only=True)
    status = (
        serializers.SerializerMethodField()
    )  # Use a SerializerMethodField for status

    class Meta:
        model = Course
        fields = "__all__"

    def get_modules_count(self, obj):
        return obj.modules.all().count()

    def get_status(self, obj):
        return obj.get_course_status_display()  # Explicitly call the method


class Moduleserializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        _class = Class.objects.get(pk=payment._class.id)
        students = _class.students.all()
        for student in students:
            StudentPayment.objects.create(
                student=student, balance=payment.amount, paid=0.0
            )
        return payment

class StudentPaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    class Meta:
        model = StudentPayment
        fields = '__all__'

    def get_student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"

    def update(self, instance, validated_data):
        action = self.context.get('action')
        index = self.context.get('index')
        amount_paid = self.context.get('amount')
        if amount_paid is None:
            raise serializers.ValidationError("The amount field is required.")
        
        current_history = instance.history or []

        if action == 'update':
            if instance.balance == 0.0:
                raise serializers.ValidationError("This student have paid fully")
            
            history = {
                "date": "",
                "amount": amount_paid,
                "changes": []
            }

            instance.balance -= amount_paid
            instance.paid += amount_paid
            current_history.append(history)
            instance.history = current_history

            instance.save()
        elif action == 'change':
            to_ch = current_history[index]
            old_amount = to_ch['amount']
            
            if old_amount != amount_paid:
                instance.balance += (old_amount - amount_paid)
                instance.paid -= (old_amount - amount_paid)

            change = {
                "date": "",
                "from": old_amount,
                "to": amount_paid
            }

            to_ch['amount'] = amount_paid
            to_ch['changes'].append(change)

            instance.history = current_history
            instance.save()

        return instance
