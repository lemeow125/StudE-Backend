from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run InitSpatialMetaData and then migrate'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute('SELECT InitSpatialMetaData(1);')

        # Call the Django migrate command
        call_command('migrate')
