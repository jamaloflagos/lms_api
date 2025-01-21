import string
import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.forms.models import model_to_dict
from datetime import date
from django.db.models.signals import post_save, post_delete
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import *

User = get_user_model()




@receiver(post_save, sender=EntranceExamScore)
def handle_entrance_exam_score_save(sender, instance, created, **kwargs):
    if not created:
        print('Yes')
        return  # Skip if the instance is not newly created

    applicant = Applicant.objects.filter(id=instance.applicant.id).first()
    print(applicant.id)
    score = instance.value
    percentage = instance.percentage  
    current_date = date.today()
    current_term = Term.objects.filter(end_date__gt=current_date).first()

    if percentage >= 50:
        # Create Parent, Student records if percentage is 50 or more
        parent, created = Parent.objects.get_or_create(
            first_name=applicant.parent_first_name,
            last_name=applicant.parent_last_name,
            contact_mail=applicant.parent_email,
            address=applicant.parent_address,
            contact_phone=applicant.parent_phone_number,
            emergency_phone=''  
        )

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

        student, created = Student.objects.get_or_create(
            first_name=applicant.first_name,
            last_name=applicant.last_name,
            _class=applicant.class_applied_for,
            parent=parent,
            email = applicant.email,
            d_o_b = applicant.d_o_b,
            gender = applicant.gender,
            # student_d=f"{applicant.first_name.index(0)}{applicant.last_name.index(0)}{applicant.d_o_b}"
        )

        if student:
            _class = student._class
            class_subjects = _class.class_subjects.all()
            for class_subject in class_subjects:
                subject = Subject.objects.filter(id=class_subject.subject.id).first()
                ScoreSheet.objects.create(student=student, subject=subject) 
            TuitionFee.objects.create(student=student, term=current_term, balance=40000.00)

            user = User.objects.filter(id=applicant.id).first()
            if user:
                user.delete()
                new_user = User.objects.create_user(id=student.id, email=applicant.email, username=f"{applicant.first_name} {applicant.last_name}", password=password, role='Student')
                if new_user:
                    student.user = new_user
                    send_email(
                        subject='Congratulations on Your Entrance Exam Score!',
                        message=f'''
                        Dear {applicant.first_name},

                        Congratulations! You have scored {score} which is {percentage}% on your entrance exam.

                        Your account has been created. Below are your login credentials:

                        Email: {user.email}
                        Password: {password}

                        Please log in and change your password as soon as possible.

                        Best regards,
                        The Admissions Team
                        ''',
                        recipient_list=[applicant.email]
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

@receiver(post_save, sender=Assignment) 
def notify_students_on_assignment(sender, instance, created, **kwargs):
    if created:
        # Notify all students in the class
        channel_layer = get_channel_layer()

        students = instance.class_subject._class.students.all() 
        for student in students:
            Notification.objects.create(
                user=student.user,
                message=f"A new assignment has been posted in: {instance.class_subject.subject.name}"
            )
        
            async_to_sync(channel_layer.group_send)(
                f"user_{student.user.id}", {
                    "type": "notifications",
                    "message": {"text": f"A new assignment has been posted in: {instance.class_subject.subject.name}"}
                }
            )

@receiver(post_save, sender=Exam) 
def notify_students_on_exam(sender, instance, created, **kwargs):
    if created:
        # Notify all students in the class
        channel_layer = get_channel_layer()

        students = instance.class_subject._class.students.all() 
        for student in students:
            notification = Notification.objects.create(
                user=student.user,
                message=f"A new exam has been posted in: {instance.class_subject.subject.name}"
            )
        
            async_to_sync(channel_layer.group_send)(
                f"user_{student.user.id}", {
                    "type": "notifications",
                    "payload": notification
                }
            )

@receiver(post_save, sender=Test) 
def notify_students_on_test(sender, instance, created, **kwargs):
    if created:
        # Notify all students in the class
        channel_layer = get_channel_layer()

        students = instance.class_subject._class.students.all() 
        for student in students:
            notification = Notification.objects.create(
                user=student.user,
                message=f"A new test has been posted in: {instance.class_subject.subject.name}"
            )
        
            async_to_sync(channel_layer.group_send)(
                f"user_{student.user.id}", {
                    "type": "notifications",
                    "payload": notification
                }
            )

@receiver(post_save, sender=Outline) 
def notify_students_on_outline(sender, instance, created, **kwargs):
    if created:
        # Notify all students in the class
        channel_layer = get_channel_layer()

        students = instance.class_subject._class.students.all() 
        for student in students:
            notification = Notification.objects.create(
                user=student.user,
                message=f"A new outline has been posted in: {instance.class_subject.subject.name}"
            )
        
            async_to_sync(channel_layer.group_send)(
                f"user_{student.user.id}", {
                    "type": "notifications",
                    "payload": notification
                }
            )

@receiver(post_save, sender=Note) 
def notify_students_on_note(sender, instance, created, **kwargs):
    if created:
        # Notify all students in the class
        channel_layer = get_channel_layer()

        students = instance.outline.class_subject._class.students.all() 
        for student in students:
            notification = Notification.objects.create(
                user=student.user,
                message=f"A new note has been posted in: {instance.outline.class_subject.subject.name}"
            )
        
            async_to_sync(channel_layer.group_send)(
                f"user_{student.user.id}", {
                    "type": "notifications",
                    "payload": notification
                }
            )

# @receiver(post_save, sender=Message)
# def notify_recipient_on_message(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         notification = Notification.objects.create(
#             user=instance.recipient,
#             message=f"You received a new message from {instance.sender.username}: {instance.content[:50]}"
#         )
    
#         async_to_sync(channel_layer.group_send)(
#                     f"user_{instance.recipient.id}", {
#                         "type": "notifications",
#                         "payload": notification
#                     }
#                 )


@receiver(post_save, sender=GroupMessage)
def notify_group_members(sender, instance, created, **kwargs):
    if created:
        group = instance.group
        sender = instance.sender
        channel_layer = get_channel_layer()

        for member in group.members.all():
            if member != sender:  # Avoid notifying the sender
                # Create a notification for each member
                user = User.objects.filter(id=member.id).first()
                notification = Notification.objects.create(
                    user=user,
                    message=f"New message in {group.name} from {sender.username}: {instance.content[:50]}"
                )

                # Send WebSocket notification
                async_to_sync(channel_layer.group_send)(
                    f"user_{member.id}", {
                        "type": "notifications",
                        "payload": notification
                    }
                )

@receiver(post_save, sender=GroupMessage)
def broadcast_group_message(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            instance.group.group_name, {
                "type": "chat_message",
                "payload": model_to_dict(instance)
            }
        )