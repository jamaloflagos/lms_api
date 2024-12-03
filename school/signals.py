import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import *


@receiver(post_save, sender=EntranceExamScore)
def handle_score_save(sender, instance, created, **kwargs):
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
            emergency_phone=''  # Adjust if necessary
        )

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

        # Create a Student record
        Student.objects.get_or_create(
            first_name=applicant.first_name,
            last_name=applicant.last_name,
            _class=applicant.class_applied_for,
            parent=parent,
            email = applicant.contact_mail,
            password = password
        )

        # Send congratulatory email
        send_email(
            subject='Congratulations on Your Entrance Exam Score!',
            message=f'''
            Dear {applicant.first_name},

            Congratulations! You have scored {score} which is {percentage}% on your entrance exam.

            Your account has been created. Below are your login credentials:

            Email: {applicant.contact_mail}
            Password: {password}

            Please log in and change your password as soon as possible.

            Best regards,
            The Admissions Team
            ''',
            recipient_list=[applicant.contact_mail]
        )
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

# @receiver(post_save, sender=Teacher)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         TeacherToken.objects.create(user=instance)

# @receiver(post_save, sender=Student)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         StudentToken.objects.create(user=instance)

