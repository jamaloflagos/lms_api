from django.contrib.auth.models import AbstractUser
from django.db import models
import shortuuid


# Create your models here. 

class User(AbstractUser):
    USER_ROLES = (
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
        ('Applicant', 'Applicant')
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES)

class Class(models.Model):
    CATEGORY_CHOICES = [
        ('Secondary', 'Secondary'),
        ('Primary', 'Primary')
    ]
    name = models.CharField(max_length=24)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    class Meta:
        db_table = "class"

    def __str__(self):
        return f"{self.name} id: {self.id}"
    
class Teacher(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    is_form_teacher = models.BooleanField(default=False)
    form_class = models.OneToOneField(Class, null=True, on_delete=models.SET_NULL, related_name="form_teacher")
    email = models.EmailField(default=None, unique=True)

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
    email = models.EmailField(default=None, unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=24)
    d_o_b = models.DateField()
    parent_first_name = models.CharField(max_length=64)
    parent_last_name = models.CharField(max_length=64)
    parent_email = models.EmailField(default=None,)
    parent_address = models.TextField()
    parent_phone_number = models.CharField(max_length=24)
    class_applied_for = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, related_name="applicants")
    has_made_payment = models.BooleanField(default=False)

    # def __str__(self):
    #     return f"class: {self.class_applied_for}"

class EntranceExamQuestion(models.Model):
    question = models.TextField()
    options = models.JSONField(default=list)
    answer = models.SmallIntegerField()

class EntranceExamScore(models.Model):
    applicant_id = models.CharField(max_length=10, unique=True)
    value = models.SmallIntegerField()
    percentage = models.SmallIntegerField()

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="students")
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, related_name="children")
    email = models.EmailField(default=None, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default=None)
    student_id = models.CharField(max_length=20)
    d_o_b = models.DateField()
 
    class Meta:
        db_table = "student"

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s email: {self.email}"
    
class Term(models.Model):
    name = models.CharField(max_length=50) 
    start_date = models.DateField()
    end_date = models.DateField()
    year =models.IntegerField(default=None)

class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} {self.id}"

class ClassSubject(models.Model):
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='class_subjects')

    class Meta:
        unique_together = ['_class', 'subject']

    def __str__(self):
        return f"{self._class.name} - {self.subject.name}"
    
class Assignment(models.Model):
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name='assignments', default=None)
    questions = models.JSONField(default=list)
    date_posted = models.DateField(auto_now_add=True)
    due_date = models.DateTimeField()
    time_allowed = models.IntegerField(default=None)
    obtainable_mark = models.IntegerField(default=10)
    
class Test(models.Model):
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name='tests', default=None)
    questions = models.JSONField(default=list)
    date_posted = models.DateField(auto_now_add=True)
    due_date = models.DateTimeField()
    time_allowed = models.IntegerField(default=None)
    obtainable_mark = models.IntegerField(default=20)

class Exam(models.Model):
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name='exams', default=None)
    questions = models.JSONField(default=list)
    date_posted = models.DateField(auto_now_add=True, null=True)
    due_date = models.DateTimeField(default=None)
    time_allowed = models.IntegerField(default=None)
    obtainable_mark = models.IntegerField(default=70)

class Score(models.Model):
    SCORE_TYPE_CHOICES = [
        ('Assignment', 'Assignment'),
        ('Test', 'Test'),
        ('Exam', 'Exam'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores", default=None)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="scores", default=None)
    score_type = models.CharField(max_length=10, choices=SCORE_TYPE_CHOICES)
    value = models.IntegerField()
    date_posted = models.DateField(auto_now_add=True, null=True)

class ScoreSheet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='score_sheets')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='score_sheets')
    assignment_score = models.IntegerField(default=0)
    test_score = models.IntegerField(default=0)
    exam_score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    grade = models.CharField(max_length=10, default=None)

    def calculate_total(self):
        self.total_score = self.assignment_score + self.test_score + self.exam_score
        if self.total_score >= 70:
            self.grade = 'Excellencce'
        elif self.total_score >= 60:
            self.grade = 'Good'
        elif self.total_score >= 40:
            self.grade = 'Fair'
        else:
            self.grade = 'Poor'
        self.save()

class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    term = models.CharField(max_length=20)
    year = models.IntegerField()
    score_sheets = models.ManyToManyField(ScoreSheet, related_name='report_cards')
    overall_total = models.IntegerField(default=0)
    overall_average = models.FloatField(default=0.0)
    teacher_comment = models.CharField(max_length=120, default=None)
    principal_comment = models.CharField(max_length=120, default=None)

    def calculate_overall(self):
        total_scores = sum(sheet.total_score for sheet in self.score_sheets.all())
        num_subjects = self.score_sheets.count()
        self.overall_total = total_scores
        self.overall_average = total_scores / num_subjects if num_subjects > 0 else 0
        self.save()

class ClassSubjectTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_subject_teachers')
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name='teachers')

    class Meta:
        unique_together = ['teacher', 'class_subject']

    def __str__(self):
        return f'{self.teacher.name} - {self.class_subject}'

class Outline(models.Model):
    title = models.CharField(max_length=100)
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name='outlines')
    week = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ['class_subject', 'week']

    def __str__(self):
        return f'Week {self.week}: {self.title} ({self.class_subject})'

class Note(models.Model):
    outline = models.ForeignKey(Outline, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=20)
    content = models.TextField()

    def __str__(self):
        return f'Note for {self.outline}'

class TuitionFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='tuition_fees')
    term = models.ForeignKey(Term, on_delete=models.PROTECT, related_name='tuition_fees')
    balance = models.FloatField()
    paid = models.FloatField(default=0.0)
    has_made_full_payment = models.BooleanField(default=False)

class Course(models.Model):
    OPEN = 'Open'
    WAITLISTED = 'Waitlisted'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (WAITLISTED, 'Waitlisted')
    ]
    
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="courses")
    creator = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="courses")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
 
class Module(models.Model):
    title = models.CharField(max_length=30)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    estimated_time = models.SmallIntegerField(default=None)

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons", default=None, null=True)
    title = models.CharField(max_length=30)
    note = models.TextField()
    has_assignment =models.BooleanField(default=False)
    assignment_questions = models.JSONField(default=list, blank=True)
    has_video = models.BooleanField(default=False)
    video = models.TextField()
    date_created = models.DateField()
    estimated_time = models.SmallIntegerField(default=None, null=True)

    def __str__(self):
        return f"{self.id}"
    
class ClassSchedule(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="class_schedules")
    topic = models.CharField(max_length=64)
    tutor = models.CharField(max_length=64)
    lesson = models.CharField(max_length=30, default=None)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Absent', 'Absent'),
        ('Present', 'Present')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances")
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="attendances", default=None)
    date_marked = models.DateField()
    status = models.CharField(max_length=7)

    class Meta:
        unique_together = ['student', 'date_marked']

class Book(models.Model):
    BOOK_LOCATION = [
        ('library', 'Library'),
        ('book_store', 'Book store')
    ]
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=64)
    copies = models.IntegerField()
    location = models.CharField(max_length=10, choices=BOOK_LOCATION)
    is_available = models.BooleanField(default=True)

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
    returned = models.BooleanField(default=False)

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
    history = models.JSONField(default=list)

    def __str__(self):
        return f"student id: {self.student} and balance : {self.balance}"

class Payment(models.Model):
    type = models.CharField(max_length=64)
    amount = models.IntegerField()
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='payments')

    class Meta:
        unique_together = ['type', '_class']


class TuitionFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='tuition_fees')
    term = models.ForeignKey(Term, on_delete=models.PROTECT, related_name='tuition_fees')
    balance = models.FloatField(default=0.0)
    paid = models.FloatField(default=0.0)
    has_made_full_payment = models.BooleanField(default=False)
