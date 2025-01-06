from rest_framework import generics
from django.http import HttpResponseBadRequest
from school.models import Book, Checkout, BookSale, BookPurchase
from school.serializers import BookSerializer, BookPurchaseSerializer,BookSaleSerializer, CheckoutSerializer

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    view_permissions = {
        'get': {'admin': True, 'teacher': True, 'student': True, 'librarian': True}
    }

    def get_queryset(self):
        location = self.request.query_params.get('location')
        queryset = super().get_queryset()

        return queryset.filter(location=location)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    view_permissions = {
        'get': {'admin': True, 'teacher': True, 'student': True, 'librarian': True}
    }

# Book Purchase Views
class BookPurchaseList(generics.ListCreateAPIView):
    queryset = BookPurchase.objects.all()
    serializer_class = BookPurchaseSerializer
    view_permissions = {
        'post,get': {'librarian': True}
    }

    def perform_create(self, serializer):
        title = self.request.data.get('title')
        author = self.request.data.get('author')
        copies = self.request.data.get('copies')
        location = self.request.data.get('location')

        book = Book.objects.create(title=title, author=author, copies=copies, location=location)
        serializer.save(book=book)


class BookPurchaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookPurchase.objects.all()
    serializer_class = BookPurchaseSerializer
    view_permissions = {
        'put,get': {'librarian': True}
    }


# Book Sale Views
class BookSaleList(generics.ListCreateAPIView):
    queryset = BookSale.objects.all()
    serializer_class = BookSaleSerializer
    view_permissions = {
        'post,get': {'librarian': True}
    }

    def perform_create(self, serializer):
        book_id = self.request.query_params.get('book_id')
        sale_quantity = serializer.validated_data.get('quantity')
        sale_unit_price = serializer.validated_data.get('unit_price')
        sale_total_price = sale_unit_price * sale_quantity
        book_sold = Book.objects.get(pk=book_id)
        book_old_available_copies = book_sold.copies

        if sale_quantity > book_old_available_copies:
            return HttpResponseBadRequest('The sale quantity is more than the available copies')
        book_new_available_copies = book_old_available_copies - sale_quantity
        book_sold.copies = book_new_available_copies
        if book_sold.copies == 0:
            book_sold.is_available = False

        serializer.save(total_price=sale_total_price)



class BookSaleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookSale.objects.all()
    serializer_class = BookSaleSerializer
    view_permissions = {
        'put,get': {'librarian': True}
    }

    def perform_update(self, serializer):
        instance = self.get_object()
        book = Book.objects.get(pk=instance.book)

        if serializer.validated_data.get('unit_price'):
            new_unit_price = validated_data.get('unit_price')
            instance.total_price = new_unit_price * instance.quantity
        elif serializer.validated_data.get('quantity'):
            new_quantity = serializer.validated_data.get('quantity')
            new_book_copies = book.copies + instance.quantity
            book.copies = new_book_copies - new_quantity
            if book.copies == 0:
                book.is_available = False

        serializer.save()

# Checkout Views
class CheckoutList(generics.ListCreateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    view_permissions = {
        'post,get': {'librarian': True}
    }

    def perform_create(self, serializer):
        book_id = serializer.validated_data.get('book')
        book = Book.objects.get(pk=book_id)
        book.copies = book.copies - 1
        if book.copies == 0:
            book.is_available = False
        
        serializer.save()



class CheckoutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    view_permissions = {
        'put,get,delete': {'librarian': True}
    }

    def perform_update(self, serializer):
        instance = self.get_object()
        if serializer.validated_data.get('returned'):
            book = instance.book
            book.copies = book.copies + 1

        serializer.save()