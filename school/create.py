import random
# import django
from school.models import EntranceExamQuestion

# Ensure your Django environment is set up
# django.setup()

# Define a list of sample question templates and options
question_templates = [
    "What is the capital of {}?",
    "Which of the following is a {}?",
    "Identify the {} from the options below.",
    "What is the result of {}?",
    "{} belongs to which category?",
]

categories = ["France", "Python programming", "fruit", "5 + 3", "biology"]

options_pool = [
    ["Paris", "London", "Berlin", "Madrid"],
    ["Function", "Class", "Variable", "Loop"],
    ["Apple", "Carrot", "Banana", "Potato"],
    ["8", "10", "7", "9"],
    ["Animal", "Plant", "Mineral", "Insect"],
]

# Function to create random questions
def create_random_questions(num_questions=20):
    for _ in range(num_questions):
        # Randomly select a question template and category
        template = random.choice(question_templates)
        category = random.choice(categories)

        # Generate a random question
        question_text = template.format(category)

        # Randomly select options
        options = random.choice(options_pool)

        # Randomly determine the correct answer index
        correct_answer_index = random.randint(0, len(options) - 1)

        # Create and save the question to the database
        question = EntranceExamQuestion(
            question=question_text,
            options=options,
            answer=correct_answer_index,
        )
        question.save()

        print(f"Created Question: {question_text}")

# Run the script to create 20 questions
# create_random_questions()
