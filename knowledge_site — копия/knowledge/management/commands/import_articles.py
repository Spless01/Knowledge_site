import os
import pandas as pd
from django.core.management.base import BaseCommand
from knowledge.models import Article, KnowledgeField


class Command(BaseCommand):
    help = "Импортирует статьи из Excel-файлов в базу данных"

    def handle(self, *args, **kwargs):
        folder_path = "knowledge/excel_files"  # Путь к папке с Excel-файлами
        files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

        if not files:
            self.stdout.write(self.style.WARNING("Excel-файлы не найдены в указанной директории."))
            return

        for file in files:
            file_path = os.path.join(folder_path, file)
            discipline_name = file.replace("_100pages.xlsx", "").replace("_", " ")

            # Получаем или создаем KnowledgeField
            field, created = KnowledgeField.objects.get_or_create(
                name=discipline_name,
                defaults={'description': f'Статьи для дисциплины {discipline_name}'}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Создано поле знаний: {discipline_name}"))

            try:
                # Чтение Excel-файла
                df = pd.read_excel(file_path)
                self.stdout.write(self.style.SUCCESS(f"Обработка файла: {file}"))

                # Добавление статей в базу данных
                for _, row in df.iterrows():
                    Article.objects.create(
                        title=row.get('Название статьи', 'Без названия'),
                        link=row.get('Ссылка', ''),
                        doi=row.get('DOI', ''),
                        author=row.get('Автор', 'Автор отсутствует'),
                        field=field  # Связь с KnowledgeField
                    )

                self.stdout.write(self.style.SUCCESS(f"Файл {file} успешно импортирован."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при обработке {file}: {e}"))
