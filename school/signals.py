import random
import string
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import *

User = get_user_model()


@receiver(post_save, sender=EntranceExamScore)
def handle_axamScore_save(sender, instance, created, **kwargs):
    if not created:
        return  # Skip if the instance is not newly created

    applicant = Applicant.objects.get(application_id=instance.applicant_id)
    score = instance.value
    percentage = instance.percentage  

    if percentage >= 50:
        # Create Parent, Student records if percentage is 50 or more
        parent, created = Parent.objects.get_or_create(
            first_name=applicant.parent_first_name,
            last_name=applicant.parent_last_name,
            contact_mail=applicant.parent_contact_mail,
            address=applicant.parent_address,
            contact_phone=applicant.parent_contact_phone,
            emergency_phone=''  
        )

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

        student = Student.objects.get_or_create(
            first_name=applicant.first_name,
            last_name=applicant.last_name,
            _class=applicant.class_applied_for,
            parent=parent,
            email = applicant.contact_mail,
        )

        if student:
            _class = student._class
            subjects = _class.class_subjects.all()
            for subject in subjects:
                ScoreSheet.objects.create(student=student, subject=subject)

            user = User.objects.create_user(email=applicant.contact_mail, username=f"{applicant.first_name} {applicant.last_name}", password=password, role='Student')
            if user:
                send_email(
                    subject='Congratulations on Your Entrance Exam Score!',
                    message=f'''
                    Dear {applicant.first_name},

                    Congratulations! You have scored {score} which is {percentage}% on your entrance exam.

                    Your account has been created. Below are your login credentials:

                    Email: {user.email}
                    Password: {user.password}

                    Please log in and change your password as soon as possible.

                    Best regards,
                    The Admissions Team
                    ''',
                    recipient_list=[applicant.contact_mail]
                )
            else: 
                pass
        else:
            pass
    else:
        # Send encouraging email if percentage is less than 50
        send_email(
            subject='Keep Trying - Your Entrance Exam Score',
            message=f'''
            Dear {applicant.first_name},

            We received your entrance exam score of {score} which is {percentage}%. 

            Don't be discouraged; keep working hard and striving for your goals.

            Best regards,
            The Admissions Team
            ''',
            recipient_list=[applicant.contact_mail]
        )

def send_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list
    )

@receiver(post_save, sender=Score)
def handle_score_save(sender, instance, created, **kwargs):
    if not created:
        return
    
    student = instance.student
    subject = instance.subject
    value = instance.value
    score_type = instance.score_type

    score_sheet = ScoreSheet.objects.filter(student=student, subject=subject).first()
    if score_sheet:
        if score_type == 'Assignment':
            score_sheet.assignment_score = value
            score_sheet.calculate_total()
        elif score_type == 'Test':
            score_sheet.test_score = value
            score_sheet.calculate_total()
        elif score_type == 'Exam':
            score_sheet.exam_score = value
            score_sheet.calculate_total()
    else:
        return

@receiver(post_delete, sender=Teacher)
def delete_associated_user(sender, instance, **kwargs):
    """
    Deletes the User instance associated with the Teacher's email
    after the Teacher instance is deleted.
    """
    try:
        user = User.objects.get(email=instance.email)
        user.delete()
    except User.DoesNotExist:
        pass  # User might not exist, ignore
