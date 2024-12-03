from rest_framework import generics
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseBadRequest
from school.models import Applicant
from school.serializers import ApplicantSerializer

class ApplicantList(generics.ListCreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer

    def perform_create(self, serializer):
        contact_mail = serializer.validated_data.get("contact_mail")

        # Check if there is an existing applicant with the same contact_mail or parent_contact_mail
        if Applicant.objects.filter(contact_mail=contact_mail).exists():
            response_message = {"contact_mail": "Email already exists"}
            return HttpResponseBadRequest(response_message)

        applicant = serializer.save()
        # Send email notification after saving the applicant
        self.send_email(applicant)

    def send_email(self, applicant):
        subject = "New Applicant Created"
        message = f"""
        You have successfully submitted your application, proceed to take your entrance exam with the link beloe

        Link: http://localhost:3000/entrance-exam/{applicant.application_id} 
        """
        recipient_list = [applicant.contact_mail]  # Or any email you want to notify
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


class ApplicantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
