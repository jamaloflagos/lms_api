from django.core.management.base import BaseCommand
from school.models import Class  # Adjust the import path according to your project structure

class Command(BaseCommand):
    help = 'Populate database with six classes: JSS1 to SS3'

    