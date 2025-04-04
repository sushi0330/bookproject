from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='susumu').exists():
            User.objects.create_superuser(
                username='susumu',
                email='',
                password='susumu680420'
            )
