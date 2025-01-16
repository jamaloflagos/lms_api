# views.py
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from school.models import Applicant, Student, TuitionFee

User = get_user_model()

@api_view(["POST"])
def verify_payment(request):
    reference = request.data.get("reference")
    email = request.data.get("email")
    amount = request.data.get("amount")
    if not reference:
        return Response({"status": "error", "message": "No reference provided"}, status=400)

    paystack_secret_key = "sk_test_5602840e2f806ff816dfcd41009d3babb454504b" 
    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {paystack_secret_key}",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["data"]["status"] == "success":
            user = User.objects.filter(email=email).first()
            if user.role == 'Applicant':
                applicant = Applicant.objects.filter(id=user.id).first()
                applicant.has_made_payment = True
            elif user.role == 'Student':
                student = Student.objects.filter(id=user.id).first()
                tuition_fee = TuitionFee.objects.filter(student=student).first()
                tuition_fee.paid += amount
                tuition_fee.balance -= tuition_fee.paid
            return Response({"status": "success", "message": "Payment verified"})
        else:
            return Response({"status": "error", "message": "Payment not successful"})
    else:
        return Response({"status": "error", "message": "Failed to verify payment"}, status=500)



# from rest_framework import generics
# from django.shortcuts import get_object_or_404
# from school.models import Student, Payment, StudentPayment, Class
# from school.serializers import PaymentSerializer, StudentPaymentSerializer

# class PaymentList(generics.ListCreateAPIView):
#     """
#     This view
#         creates a payment for a class
#         gets all payment of a class
#     """

#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer

#     def get_queryset(self):
#         class_id = self.kwargs.get("class_id")
#         # type = self.kwargs.get('type')
#         queryset = Payment.objects.filter(_class=class_id)

#         return queryset


# class StudentPaymentList(generics.ListCreateAPIView):
#     """
#     This view
#         gets all payments made by students in a class
#     """

#     queryset = StudentPayment.objects.all()
#     serializer_class = StudentPaymentSerializer
#     http_method_names = ["get", "put", "patch", "delete"]

#     def get_queryset(self):
#         class_id = self.kwargs.get("class_id")
#         type = self.kwargs.get("type")
#         print(type)

#         _class = get_object_or_404(Class, pk=class_id)

#         students = Student.objects.filter(
#             _class=_class, _class__payments__type="Tuition fee"
#         )

#         # Now filter StudentPayment for those students
#         student_payments = StudentPayment.objects.filter(student__in=students)

#         return student_payments


# class StudentPaymentDetail(generics.RetrieveUpdateDestroyAPIView):
#     """
#     This view
#         retrieve, delete and update payment made by a student
#     """

#     queryset = StudentPayment.objects.all()
#     serializer_class = StudentPaymentSerializer

#     def get_serializer_context(self):
#         index = self.request.query_params.get("index")
#         context = super().get_serializer_context()
#         context["action"] = self.kwargs["action"]
#         context["amount"] = self.request.data.get("amount")
#         if index:
#             context["index"] = int(index)
#         return context

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

