from rest_framework import generics
from django.http import Http404
from school.models import Class, UnitTest, Exam, ClassSchedule
from school.serializers import (
    ClassSerializer, StudentSerializer,
    LessonSerializer, CourseSerializer,
    Moduleserializer, ExamSerializer,
    UnitTestSerializer, ClassScheduleSerializer
    )


# class ClassCourseList(generics.ListAPIView):
#     queryset = Class.objects.all()
#     serializer_class = ClassSerializer

#     def get_queryset(self):
#         class_id = self.request.query_params.get("class_id")
#         _class = Class.objects.get(id=class_id)
#         queryset = _class.courses.all()

#         return queryset


# class ClassStudentList(generics.ListAPIView):
#     queryset = Class.objects.all()
#     serializer_class = ClassSerializer

#     def get_queryset(self):
#         class_id = self.request.query_params.get("class_id")
#         _class = Class.objects.get(id=class_id)
#         queryset = _class.students.all()

#         return queryset

class ClassList(generics.ListCreateAPIView):
    """
    This view
      creates a new class
      get all classes
      get all students of a class
      get all courses offered by a class
      get all modules of each course offered by a class
      get all lessons of each modules of each courses offered by a class
      get all assignmnets of a class
      get all exams of a class
    """

    viewpermissions = {
        'post': {'admin': True},
        'get': {'teacher': True, 'admin': True, 'student': True}
    }

    def get_serializer_class(self):

        data_type = self.kwargs.get("data_type")

        if self.request.method == "GET":
            if data_type == "students":
                return StudentSerializer
            elif data_type == "courses":
                return CourseSerializer
            elif data_type == "modules":
                return Moduleserializer
            elif data_type == "lessons":
                return LessonSerializer
            elif data_type == "assignments":
                return UnitTestSerializer
            elif data_type == "exams":
                return ExamSerializer
            elif data_type == "clas-schedules":
                return ClassScheduleSerializer
            else:
                return ClassSerializer
        return ClassSerializer

    def get_queryset(self):
        class_id = self.kwargs.get("class_id")

        if class_id:
            _class = Class.objects.get(pk=class_id)
            data_type = self.kwargs.get("data_type")
            course_id = self.kwargs.get("course_id")
            module_id = self.kwargs.get("module_id")

            if data_type == "students":
                return _class.students.all()
            elif data_type == "courses":
                return _class.courses.all()
            elif data_type == "modules":
                course = _class.courses.get(pk=course_id)
                modules = course.modules.all()
                return modules
            elif data_type == "lessons":
                course = _class.courses.get(pk=course_id)
                module = course.modules.get(pk=module_id)
                lessons = module.lessons.all()
                return lessons
            elif data_type == "tests":
                # Get all lessons across all courses and modules for the class
                # lessons = Lesson.objects.filter(module__course___class=class_id)
                # Get all assignments related to those lessons
                return UnitTest.objects.filter(module__course___class=class_id)
            elif data_type == "exams":
                exams = Exam.objects.filter(course___class=class_id)
                return exams
            elif data_type == "class-schedules":
                exams = ClassSchedule.objects.filter(course___class=class_id)
                return exams
            else:
                return Http404("Invalid URL segment. Use 'courses' or 'students'.")

        return Class.objects.all()


class ClassDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

