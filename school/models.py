from django.db import models
from rest_framework.authtoken.models import Token as DefaultToken
import shortuuid


# Create your models here. 
class Class(models.Model):
    name = models.CharField(max_length=24)
    nick_name = models.CharField(max_length=24)
    category = models.CharField(max_length=24)

    class Meta:
        db_table = "class"

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    subjects = models.JSONField(blank=True, default=list)
    is_form_teacher = models.BooleanField(default=False)
    _class = models.OneToOneField(Class, null=True, on_delete=models.SET_NULL, related_name="form_teacher")
    email = models.EmailField(default=None, unique=True)
    password = models.CharField(max_length=64, default=None, null=True)

    class Meta:
        db_table = "teacher"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Parent(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    contact_mail = models.EmailField(default=None)
    address = models.TextField()
    contact_phone = models.CharField(max_length=24)
    emergency_phone = models.CharField(max_length=24)

    class Meta:
        db_table = "parent"

class Applicant(models.Model):
    application_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    contact_mail = models.EmailField(default=None, unique=True)
    address = models.TextField()
    contact_phone = models.CharField(max_length=24)
    parent_first_name = models.CharField(max_length=64)
    parent_last_name = models.CharField(max_length=64)
    parent_contact_mail = models.EmailField(default=None,)
    parent_address = models.TextField()
    parent_contact_phone = models.CharField(max_length=24)
    class_applied_for = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, related_name="applicants")

    def __str__(self):
        return f"class: {self.class_applied_for}"

class EntranceExamQuestion(models.Model):
    question = models.TextField()
    options = models.JSONField(default=list)
    answer = models.SmallIntegerField()

class EntranceExamScore(models.Model):
    applicant_id = models.CharField(max_length=10, unique=True)
    value = models.SmallIntegerField()
    percentage = models.SmallIntegerField()

class Student(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="students")
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, related_name="children")
    email = models.EmailField(default=None, unique=True)
    password = models.CharField(max_length=64, default=None)
 
    class Meta:
        db_table = "student"

class Course(models.Model):
    OPEN = 'O'
    WAITLISTED = 'W'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (WAITLISTED, 'Waitlisted')
    ]
    
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="courses")
    creator = models.CharField(max_length=64)
    course_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=OPEN)
 
class Module(models.Model):
    title = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    estimated_time = models.SmallIntegerField(default=None)

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons", default=None, null=True)
    title = models.CharField(max_length=30)
    note = models.TextField()
    has_unit_test =models.BooleanField(default=False)
    unit_test = models.JSONField(default=list, blank=True)
    has_video = models.BooleanField(default=False)
    video = models.TextField()
    date_created = models.DateField()
    estimated_time = models.SmallIntegerField(default=None, null=True)

    def __str__(self):
        return f"{self.id}"

    
class UnitTest(models.Model):
    module = models.OneToOneField(Module, on_delete=models.CASCADE, related_name="tests")
    status = models.CharField(max_length=30)
    due_date = models.DateField()
    due_time = models.TimeField()
    obtainable_mark = models.IntegerField()
    tota_obtainable_mark = models.IntegerField()
    questions = models.JSONField(default=list)

    def __str__(self):
        return f"{self.lesson} {self.status}"

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exams")
    date = models.DateField()
    category = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    obtainable_score = models.IntegerField()


class ClassSchedule(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="class_schedules")
    topic = models.CharField(max_length=64)
    tutor = models.CharField(max_length=64)
    lesson = models.CharField(max_length=30, default=None)

class Score(models.Model): 
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores", default=None)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_scores', null=True)
    assignment = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignment_scores', null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='test_scores', null=True)
    value = models.IntegerField()
    date_submitted = models.DateField()
    score_type = models.CharField(max_length=10)

class Grade(models.Model):
    subject = models.CharField(max_length=64)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    value = models.IntegerField()

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances")
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="attendances", default=None)
    date_marked = models.DateField()
    status = models.CharField(max_length=7)

    class Meta:
        unique_together = ['student', 'date_marked']

class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=64)
    copies = models.IntegerField()
    location = models.CharField(max_length=10)

class BookPurchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="purchases")
    date_purchased = models.DateTimeField()
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    supplier = models.CharField(max_length=30)

class BookSale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sales")
    date_sold = models.DateTimeField()
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="books")

class Checkout(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="checkouts")
    date_checked_out = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="book_borrowed")
    days_requested = models.IntegerField()

class StudyGroup(models.Model):
    name = models.CharField(max_length=255)
    group_name = models.CharField(max_length=128, blank=True, default=shortuuid.uuid)
    description = models.TextField(blank=True)
    students = models.ManyToManyField(Student, related_name='study_groups', blank=True)
    students_online = models.ManyToManyField(Student, related_name='online_in_groups', blank=True)
    creator = models.ForeignKey(Student, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_groups")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(Student, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class StudentPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    balance = models.FloatField()
    paid = models.FloatField()
    history = models.JSONField(default=dict)

class Payment(models.Model):
    type = models.CharField(max_length=64)
    amount = models.IntegerField()
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='payments')

    class Meta:
        unique_together = ['type', '_class']

# class TeacherToken(models.Model):
#     key = models.CharField("Key", max_length=40, primary_key=True)
#     user = models.OneToOneField(
#         'Teacher',
#         related_name='auth_token',
#         on_delete=models.CASCADE,
#     )
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Teacher Token"
#         verbose_name_plural = "Teacher Tokens"

#     def save(self, *args, **kwargs):
#         if not self.key:
#             self.key = self.generate_key()
#         return super().save(*args, **kwargs)

#     def generate_key(self):
#         return binascii.hexlify(os.urandom(20)).decode()

#     def __str__(self):
#         return self.key

# class StudentToken(DefaultToken):
#     user = models.OneToOneField(
#         'Teacher',
#         related_name='auth_token',
#         on_delete=models.CASCADE,
#     )

#     class Meta:
#         abstract = False