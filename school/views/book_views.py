from rest_framework import generics
from school.models import Book, Checkout, BookSale, BookPurchase
from school.serializers import BookSerializer, BookPurchaseSerializer,BookSaleSerializer, CheckoutSerializer

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# Book Purchase Views
class BookPurchaseList(generics.ListCreateAPIView):
    queryset = BookPurchase.objects.all()
    serializer_class = BookPurchaseSerializer


class BookPurchaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookPurchase.objects.all()
    serializer_class = BookPurchaseSerializer


# Book Sale Views
class BookSaleList(generics.ListCreateAPIView):
    queryset = BookSale.objects.all()
    serializer_class = BookSaleSerializer


class BookSaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookSale.objects.all()
    serializer_class = BookSaleSerializer


# Checkout Views
class CheckoutList(generics.ListCreateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer


class CheckoutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

