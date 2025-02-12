from rest_framework import generics
from school.models import Score, ScoreSheet, ReportCard, Student, Subject, Class, Term
from school.serializers import ScoreSerializer, ScoreSheetSerializer, ReportCardSerializer

class ScoreList(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    view_permissions = {
        'get': {'teacher': True, 'student': True, 'admin': True},
        'post': {'student': True}
    }

    def get_queryset(self):
        queryset = Score.objects.all()

        student_id = self.request.query_params.get("student_id")
        subject_id = self.request.query_params.get("subject_id")
        if subject_id and student_id:
            student = Student.objects.filter(id=student_id).first()
            subject = Subject.objects.filter(id=subject_id).first()
            if student and subject:
                queryset = Score.objects.filter(student=student, subject=subject)
            else:
                queryset = Score.objects.none()

        return queryset


class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    view_permissions = {
        'get': {'teacher': True, 'student': True, 'admin': True}
    }


class ScoreSheetList(generics.ListAPIView):
    serializer_class = ScoreSheetSerializer
    view_permissions = {
        'get': {'teacher': True, 'student': True, 'admin': True}
    }

    def get_queryset(self):
        queryset = ScoreSheet.objects.all()

        student_id = self.request.query_params.get('student_id')
        class_id = self.request.query_params.get('class_id')
        if student_id:
            student = Student.objects.filter(id=student_id).first()
            if student:
                queryset = ScoreSheet.objects.filter(student=student)
            else:
                queryset = ScoreSheet.objects.none()
        elif class_id:
            _class = Class.objects.filter(id=class_id).first()
            if _class:
                students = _class.students.all()
                queryset = ScoreSheet.objects.filter(student__in=students)
            else:
                queryset = ScoreSheet.objects.none()
        
        return queryset
    

class ReportCardList(generics.ListCreateAPIView):
    serializer_class = ReportCardSerializer
    view_permissions = {
        'get': {'teacher': True, 'student': True, 'admin': True},
        'post': {'teacher': True}
    }

    def get_queryset(self):
        queryset = ReportCard.objects.all()

        class_id = self.request.query_params.get('class_id')
        term_id = self.request.query_params.get('term_id')
        if class_id and term_id:
            _class = Class.objects.filter(id=class_id).first()
            term = Term.objects.filter(id=term_id).first()
            if _class:
                students = _class.students.all()
                queryset = ReportCard.objects.filter(student__in=students, term=term)
            else:
                queryset = ReportCard.objects.none()
        
        return queryset
    
    def perform_create(self, serializer):
        class_id = self.request.data.get('class_id')
        term_id = self.request.data.get('term_id')
        
        if class_id and term_id:
            _class = Class.objects.filter(id=class_id).first()
            if _class:
                term = Term.objects.filter(id=term_id).first()
                students = _class.students.all()
                for student in students:
                    report_card = serializer.save(student=student, term=term.name, year=term.year)
                    score_sheets = ScoreSheet.objects.filter(student=student)
                    report_card.score_sheets.add(*score_sheets)
                    report_card.calculate_overall()
            else:
                pass 
        else:
            pass

class ReportCardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReportCard.objects.all()
    lookup_field = 'student'
    serializer_class = ReportCardSerializer
    view_permissions = {
        'get': {'teacher': True, 'student': True, 'admin': True},
        'put': {'teacher': True}
    }

