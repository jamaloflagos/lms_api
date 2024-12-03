from rest_framework import generics
from django.shortcuts import get_object_or_404
from school.models import Student, Payment, StudentPayment, Class
from school.serializers import PaymentSerializer, StudentPaymentSerializer

class PaymentList(generics.ListCreateAPIView):
    """
    This view
        creates a payment for a class
        gets all payment of a class
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        # type = self.kwargs.get('type')
        queryset = Payment.objects.filter(_class=class_id)

        return queryset


class StudentPaymentList(generics.ListCreateAPIView):
    """
    This view
        gets all payments made by students in a class
    """

    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer
    http_method_names = ["get", "put", "patch", "delete"]

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")
        type = self.kwargs.get("type")
        print(type)

        _class = get_object_or_404(Class, pk=class_id)

        students = Student.objects.filter(
            _class=_class, _class__payments__type="Tuition fee"
        )

        # Now filter StudentPayment for those students
        student_payments = StudentPayment.objects.filter(student__in=students)

        return student_payments


class StudentPaymentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    This view
        retrieve, delete and update payment made by a student
    """

    queryset = StudentPayment.objects.all()
    serializer_class = StudentPaymentSerializer

    def get_serializer_context(self):
        index = self.request.query_params.get("index")
        context = super().get_serializer_context()
        context["action"] = self.kwargs["action"]
        context["amount"] = self.request.data.get("amount")
        if index:
            context["index"] = int(index)
        return context

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

