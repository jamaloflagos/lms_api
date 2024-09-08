import random
from datetime import datetime, timedelta
from school.models import Class, Course, Module, Lesson, Assignment

# Helper function to create unit tests
def generate_unit_tests():
    unit_tests = []
    for i in range(5):
        unit_test = {
            "question": f"Sample Question {i + 1}",
            "options": [f"Option {j + 1}" for j in range(4)],  # 4 options per question
            "answer": random.randint(0, 3)  # Randomly pick an index for the correct answer
        }
        unit_tests.append(unit_test)
    return unit_tests

# Create 5 courses for each class (with IDs from 1 to 6)
def create_courses():
    for class_id in range(1, 7):
        _class = Class.objects.get(id=class_id)
        for i in range(5):  # Create 5 courses per class
            Course.objects.create(
                title=f"Course {i + 1} for Class {class_id}",
                description=f"Description for Course {i + 1} for Class {class_id}",
                picture=f"course_{i + 1}_image.jpg",
                _class=_class,
                creator="Admin"
            )
    print("Courses created successfully.")

# Create 5 modules for each course
def create_modules():
    courses = Course.objects.all()
    for course in courses:
        for i in range(5):  # Create 5 modules per course
            Module.objects.create(
                title=f"Module {i + 1} for {course.title}",
                course=course,
                estimated_time=random.randint(30, 120)  # Random estimated time (minutes)
            )
    print("Modules created successfully.")

# Create 5 lessons for each module with unit tests
def create_lessons():
    modules = Module.objects.all()
    current_date = datetime.now().date()
    for module in modules:
        for i in range(5):  # Create 5 lessons per module
            Lesson.objects.create(
                module=module,
                title=f"Lesson {i + 1} for {module.title}",
                note=f"Notes for Lesson {i + 1} of {module.title}",
                has_unit_test=True,
                unit_test=generate_unit_tests(),  # Generate 5 unit tests per lesson
                has_video=True,
                video=f"http://example.com/video_lesson_{i + 1}.mp4",
                date_created=current_date,
                estimated_time=random.randint(20, 60)  # Random estimated time (minutes)
            )
    print("Lessons created successfully.")

# Create 3 assignments for 3 lessons (per class can only have 3 assignments)
def create_assignments():
    lessons = Lesson.objects.all()[:3]  # Only create assignments for the first 3 lessons
    current_date = datetime.now().date()
    for i, lesson in enumerate(lessons):
        Assignment.objects.create(
            lesson=lesson,
            status="Active",
            due_date=current_date + timedelta(days=7 + i),  # Set due date 7, 8, 9 days from now
            due_time=(datetime.now() + timedelta(hours=2)).time(),
            obtainable_score=100,
            questions=generate_unit_tests()  # Using unit tests as sample assignment questions
        )
    print("Assignments created successfully.")

# Master function to call all the creation functions
def create_all_data():
    create_courses()
    create_modules()
    create_lessons()
    create_assignments()

# Run the master function to populate the database
create_all_data()
