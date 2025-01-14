from school.models import Subject, Class, Teacher, Outline, ClassSubject, Note, Assignment, Test, Exam
from school.serializers import SubjectSerializer, OutlineSerializer, NoteSerializer, ClassSubjectSerializer, AssignmentSerializer, TestSerializer, ExamSerializer
from rest_framework import generics

# class SubjectList(generics.ListAPIView):
#     serializer_class = SubjectSerializer
#     view_permissions = {
#         'get': {'admin': True, 'teacher': True, 'student': True}
#     }

#     def get_queryset(self):
#         queryset = Subject.objects.all()
#         class_id = self.request.query_params.get('class_id')
#         teacher_id = self.request.query_params.get('teacher_id')

#         if class_id:
#             _class = Class.objects.get(id=class_id)
#             queryset = Subject.objects.filter(class_subjects___class=_class).distinct()
#         elif teacher_id:
#             teacher = Teacher.objects.get(id=teacher_id)
#             queryset = ClassSubject.objects.filter(teachers__teacher=teacher).select_related('_class', 'subject')
        
#         return queryset

class SubjectList(generics.ListAPIView):
    serializer_class = SubjectSerializer  # Default serializer
    view_permissions = {
        'get': {'admin': True, 'teacher': True, 'student': True}
    }

    def get_serializer_class(self):
        teacher_id = self.request.query_params.get('teacher_id')
        if teacher_id:
            return ClassSubjectSerializer  # Use ClassSubjectSerializer for teacher queries
        return SubjectSerializer  # Default serializer

    def get_queryset(self):
        queryset = Subject.objects.all()  # Default queryset
        class_id = self.request.query_params.get('class_id')
        teacher_id = self.request.query_params.get('teacher_id')

        if class_id:
            # Filter subjects by class ID
            _class = Class.objects.filter(id=class_id).first()
            if _class:
                queryset = Subject.objects.filter(class_subjects___class=_class).distinct()
            else:
                queryset = Subject.objects.none()
        elif teacher_id:
            # Filter ClassSubject by teacher ID
            teacher = Teacher.objects.filter(id=teacher_id).first()
            if teacher:
                queryset = ClassSubject.objects.filter(teachers__teacher=teacher).select_related('_class', 'subject')
            else:
                queryset = ClassSubject.objects.none()

        return queryset

    
            # queryset = Subject.objects.filter(class_subjects__teachers__teacher=teacher).distinct() 
class OutlineList(generics.ListCreateAPIView):
    serializer_class = OutlineSerializer
    view_permissions = {
        'get,post': {'admin': True, 'teacher': True, 'student': True}
    }

    def get_queryset(self):
        queryset = Outline.objects.all()

        class_id = self.request.query_params.get('class_id')
        subject_id = self.request.query_params.get('subject_id')
        if class_id and subject_id:
            _class = Class.objects.filter(id=class_id).first() 
            subject = Subject.objects.filter(id=subject_id).first()
            if _class and subject:
                class_subject = ClassSubject.objects.filter(_class=_class, subject=subject).first()
                if class_subject:
                    queryset = Outline.objects.filter(class_subject___class=_class, class_subject__subject=subject).order_by('week')
                else:
                    queryset = Outline.objects.none()
            else:
                queryset = Outline.objects.none()

        return queryset
    
    def perform_create(self, serializer):
        class_id = self.request.data.get('class_id')
        subject_id = self.request.data.get('subject_id')
        
        _class = Class.objects.filter(id=class_id).first()
        subject = Class.objects.filter(id=subject_id).first()
        if _class and subject:
            class_subject = ClassSubject.objects.filter(_class=_class, subject=subject).first()
            if class_subject:
                serializer.save(class_subject=class_subject)
            else:
                pass
        else:
            pass

class OutlineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outline.objects.all()
    serializer_class = OutlineSerializer

class NoteList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.all()
        outline_id = self.request.query_params.get('outline_id')

        if outline_id:
            outline = Outline.objects.filter(id=outline_id).first()
            if outline:
                queryset = outline.notes.all()
            else:
                queryset = Note.objects.none()

        return queryset
    
class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class AssignmentList(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        queryset = Assignment.objects.all()

        class_id = self.request.query_params.get('class_id')
        subject_id = self.request.query_params.get('subject_id')
        if class_id and subject_id:
            _class = Class.objects.filter(id=class_id).first()
            subject = Subject.objects.filte(id=subject_id).first()
            if _class and subject:
                class_subject = ClassSubject.objects.filter(_class=_class, subject=subject).first()
                if class_subject:
                    queryset = Assignment.objects.filter(class_subject__subject=subject, class_subject___class=_class).order_by('date_posted')
                else: 
                    queryset = Assignment.objects.none()
            else:
                queryset = Assignment.objects.none()

        return queryset
    
    def perform_create(self, serializer):
        class_id = self.request.data.get('class_id')
        subject_id = self.request.data.get('subject_id')
        
        _class = Class.objects.filter(id=class_id).first()
        subject = Class.objects.filter(id=subject_id).first()
        if _class and subject:
            class_subject = ClassSubject.objects.filter(_class=_class, subject=subject).first()
            if class_subject:
                serializer.save(class_subject=class_subject)
            else:
                pass
        else:
            pass

class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class TestList(generics.ListCreateAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        queryset = Test.objects.all()

        class_id = self.request.query_params.get('class_id')
        subject_id = self.request.query_params.get('subject_id')
        if class_id and subject_id:
            _class = Class.objects.filter(id=class_id).first()
            subject = Subject.objects.filte(id=subject_id).first()
            if _class and subject:
                class_subject = ClassSubject.objects.filter(_class=_class, subject=subject).first()
                if class_subject:
                    queryset = Test.objects.filter(class_subject__subject=subject, class_subject___class=_class).order_by('date_posted')
                else:
                    queryset = Test.objects.none()
            else:
                queryset = Test.objects.none()

        return queryset
    
    def perform_create(self, serializer):
        class_id = self.request.data.get('class_id')
        subject_id = self.request.data.get('subject_id')
        
        _class = Class.objects.filter(id=class_id).first()
        subject = Class.objects.filter(id=subject_id).first()
        if _class and subject:
            class_subject = ClassSubject.objects.filter(_class=_class, subject=subject).first()
            if class_subject:
                serializer.save(class_subject=class_subject)
            else:
                pass
        else:
            pass

class TestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class ExamList(generics.ListCreateAPIView):
    serializer_class = ExamSerializer

    def get_queryset(self):
        queryset = Exam.objects.all()

        class_id = self.request.query_params.get('class_id')
        subject_id = self.request.query_params.get('subject_id')
        if class_id and subject_id:
            _class = Class.objects.filter(id=class_id).first()
            subject = Subject.objects.filte(id=subject_id).first()
            if _class and subject:
                class_subject = ClassSubject.objects.filter(_class=_class, subject=subject).first()
                if class_subject:
                    queryset = Exam.objects.filter(class_subject__subject=subject, class_subject___class=_class).order_by('date_posted')
                else:
                    queryset = Exam.objects.none()
            else:
                queryset = Exam.objects.none()

        return queryset
    
    def perform_create(self, serializer):
        class_id = self.request.data.get('class_id')
        subject_id = self.request.data.get('subject_id')

        _class = Class.objects.filter(id=class_id).first()
        subject = Class.objects.filter(id=subject_id).first()
        if _class and subject:
            class_subject = ClassSubject.objects.filter(_class=_class, subject=subject).first()
            if class_subject:
                serializer.save(class_subject=class_subject)
            else:
                pass
        else:
            pass

class ExamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer