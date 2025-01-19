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
    students = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = "__all__"

    def get_students(self, obj):
        student_count = obj.students.count()
        return student_count

class TeacherSerializer(serializers.ModelSerializer):
    form_class = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(), write_only=True, required=False
    )
    form_class_details = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = "__all__"

    def get_form_class_details(self, obj):
            if obj.form_class:
                return {"id": obj.form_class.id, "name": obj.form_class.name}
            return None
    
    def get_subjects(self, obj):
            # Fetch all ClassSubjectTeacher entries for this teacher
            class_subject_teachers = obj.class_subject_teachers.select_related('class_subject', 'class_subject__subject', 'class_subject___class')
            
            subjects_dict = {}
            for entry in class_subject_teachers:
                subject_name = entry.class_subject.subject.name
                class_name = entry.class_subject._class.name

                if subject_name not in subjects_dict:
                    subjects_dict[subject_name] = {
                        "name": subject_name,
                        "classes": []
                    }
                
                subjects_dict[subject_name]["classes"].append(class_name)

            return list(subjects_dict.values())

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ClassSubjectSerializer(serializers.ModelSerializer):
    class_id = serializers.IntegerField(source='_class.id')  
    class_name = serializers.CharField(source='_class.name')  
    subject_id = serializers.IntegerField(source='subject.id')  
    subject_name = serializers.CharField(source='subject.name') 

    class Meta:
        model = ClassSubject
        fields = ['class_id', 'class_name', 'subject_id', 'subject_name']

class OutlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outline
        fields = '__all__'
        extra_kwargs = {
            'class_subject': {'required': False},
        }

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        extra_kwargs = {
            'outline': {'required': False},
        }

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        extra_kwargs = {
            'class_subject': {'required': False},
        }

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
        extra_kwargs = {
            'class_subject': {'required': False},
        }
        
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'
        extra_kwargs = {
            'class_subject': {'required': False},
        }

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

class ScoreSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreSheet
        fields = '__all__'
        read_only_field = ['__all__']

class ReportCardSerializer(serializers.ModelSerializer):
    teacher_comment = serializers.CharField(required=False)
    principal_comment = serializers.CharField(required=False)
    
    class Meta:
        model = ReportCard
        fields = '__all__'
        read_only_field = ['__all__']

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'

class TuitionFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuitionFee
        fields = '__all__'

class StudyGroupSerializer(serializers.ModelSerializer):
    creator_details = serializers.SerializerMethodField()
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ["group_name", "created_at"]

    def create(self, validated_data):
        creator = validated_data.get("creator")
        # student = Student.objects.get(id=creator)
        group = Group.objects.create(**validated_data)
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

class ClassScheduleSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = ClassSchedule
        fields = "__all__"

    def get_course(self, obj):
        return f"{obj.course.title}"

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    # _class = serializers.CharField(write_only=True)
    # class_details = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    # def get_class_details(self, obj):
    #     return {
    #         "id": obj._class.id,
    #         "name": obj._class.name
    #     }

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
    classes = serializers.JSONField(write_only=True)
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ['_class']

    def create(self, validated_data):
        classes = validated_data.get('classes')
        type = validated_data.get('type')
        amount = validated_data.get('amount')

        for _class in list(classes):
            _class = Class.objects.get(pk=_class)
            payment = Payment.objects.create(type=type, amount=amount, _class=_class)
            students = Class.objects.get(pk=payment._class.id).students.all()
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
        amount_paid = float(self.context.get('amount'))
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

class BookPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPurchase
        field = 'field'