from django.core.management.base import BaseCommand
from wb.parser import start

class Command(BaseCommand):
    help = 'Парсинг товаров с WB по категории или по запросу'

    def handle(self, *args, **kwargs):
        start()
        self.stdout.write(self.style.SUCCESS('Парсинг завершён'))