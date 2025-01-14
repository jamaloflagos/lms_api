from rest_framework import generics
from school.models import Score, ScoreSheet, ReportCard, Student, Subject, Class, Term
from school.serializers import ScoreSerializer, ScoreSheetSerializer, ReportCardSerializer

class ScoreList(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        queryset = Score.objects.all()

        student_id = self.request.query_params.get("student_id")
        subject_id = self.request.query_params.get("subject_id")
        score_type = self.request.query_params.get("score_type")
        if subject_id and student_id and score_type:
            student = Student.objects.filter(id=student_id).first()
            subject = Subject.objects.filter(id=subject_id).first()
            if student and subject:
                queryset = Score.objects.filter(student=student, subject=subject, score_type=score_type)
            else:
                queryset = Score.objects.none()

        return queryset


class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


class ScoreSheetList(generics.ListAPIView):
    serializer_class = ScoreSheetSerializer

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

    def get_queryset(self):
        queryset = ReportCard.objects.all()

        class_id = self.request.query_params.get('class_id')
        if class_id:
            _class = Class.objects.filter(id=class_id).first()
            if _class:
                students = _class.students.all()
                queryset = ReportCard.objects.filter(student__in=students)
            else:
                queryset = ReportCard.objects.none()
        
        return queryset
    
    def perform_create(self, serializer):
        class_id = self.request.data.get('class_id')
        term_start_date = self.request.data.get('term_start_date')
        term_end_date = self.request.data.get('term_end_date')
        if class_id and term_start_date and term_end_date:
            _class = Class.objects.filter(id=class_id).first()
            if _class:
                term = Term.objects.filter(start_date=term_start_date, end_date=term_end_date)
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

