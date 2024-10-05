from django.urls import path
from .views import *

# api endpoints

urlpatterns = [
    path('std_payment/<int:class_id>/<str:type>', StudentPaymentList.as_view(), name='std_payment'),
    path('std-payment/<int:pk>/<str:action>', StudentPaymentDetail.as_view(), name='std_payment'),
    path('payment/', PaymentList.as_view(), name='payment'),
    path('payment/<int:class_id>/<str:type>', PaymentList.as_view(), name='payment'),
    path('login/', LoginView.as_view(), name='login'),
    path('course/', CourseList.as_view(), name='course'), 
    path('course/<int:pk>', CourseDetail.as_view(), name='course-detail'), 
    path('module', ModuleList.as_view(), name='module'), 
    path('groups/', StudyGroupList.as_view(), name='groups'),
    path('groups/<int:pk>/<int:student_id>', StudyGroupDetail.as_view(), name='groups'),
    path('groups/<int:group_id>/<str:data_type>', StudyGroupInfoList.as_view(), name='groups'),
    path('entrance-exam-questions/', EntranceExamQuestionList.as_view(), name='entrance-exam-questions'),
    path('entrance-exam-score/', EntranceExamScoreList.as_view(), name='entrance-exam-score'),
    path('entrance-exam-score/<str:applicant_id>/', EntranceExamScoreDetail.as_view(), name='entrance-exam-score'),
    path('questions/', QuestionList.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('applicants/', ApplicantList.as_view(), name='applicant-list'),
    path('applicants/<int:pk>/', ApplicantDetail.as_view(), name='applicant-detail'),
    path("students/", StudentList.as_view(), name="student-list"),
    path("students/<int:student_id>/<str:data_type>", StudentInfoList.as_view(), name="student-list"),
    path("students/<int:pk>/", StudentDetail.as_view(), name="student-detail"),
    path("class/", ClassList.as_view(), name="class-list"),
    path("class/<int:class_id>/<str:data_type>", ClassList.as_view(), name="class-list"),
    path("class/<int:class_id>/courses/<int:course_id>/<str:data_type>", ClassList.as_view(), name="class-list"),
    path("class/<int:class_id>/courses/<int:course_id>/modules/<int:module_id>/<str:data_type>", ClassList.as_view(), name="class-list"),
    path("class/<int:class_id>/courses/<int:course_id>/modules/<int:module_id>/lessons/<int:lesson_id>", ClassList.as_view(), name="class-list"),
    path("class/<int:pk>/", ClassDetail.as_view(), name="class-detail"),
    path("teachers/", TeacherList.as_view(), name="teacher-list"),
    path("teachers/<int:pk>/", TeacherDetail.as_view(), name="teacher-detail"),
    path("parents/", ParentList.as_view(), name="parent-list"),
    path("parents/<int:pk>/", ParentDetail.as_view(), name="parent-detail"),
    path("lessons/", LessonList.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetail.as_view(), name="lesson-detail"),
    path("scores", ScoreList.as_view(), name="score-list"),
    path("score", ScoreDetail.as_view(), name="score-list"),
    path("grades/", GradeList.as_view(), name="grade-list"),
    path("grades/<int:student_id>/<int:subject_id>/", GradeDetail.as_view(), name="grade-detail"),
    path("attendances/", AttendanceList.as_view(), name="attendance-list"),
    path("attendances/<int:pk>/", AttendanceDetail.as_view(), name="attendance-detail"),
    path("books/", BookList.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetail.as_view(), name="book-detail"),
    path("book_sales/", BookSaleList.as_view(), name="book_sale-list"),
    path("book_sales/<int:pk>/", BookSaleDetail.as_view(), name="book_sale-detail"),
    path("book_purchases/", BookPurchaseList.as_view(), name="book_purchase-list"),
    path(
        "book_purchases/<int:pk>/",
        BookPurchaseDetail.as_view(),
        name="book_purchase-detail",
    ),
    path("checkouts/", CheckoutList.as_view(), name="checkout-list"),
    path("checkouts/<int:pk>/", CheckoutDetail.as_view(), name="checkout-detail"),
]