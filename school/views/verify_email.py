from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
User = get_user_model()


@api_view(["POST"])
def verify_email(request):
    email = request.data.get("email")
    if not email:
        return HttpResponseBadRequest({"message": "No Email provided"})

    # Simulated validation: Check if the email is in the valid email list
    if User.objects.filter(email=email).exists():
         return Response({"message": "Email is valid"})
    else:
            response_message = {"message": "Invalid email! \n You can only make payment with your registered student email or registered applicant email"}
            return HttpResponseBadRequest(response_message)
         
