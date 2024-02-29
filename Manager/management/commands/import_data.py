import openpyxl
from django.core.management.base import BaseCommand
from Manager.models import Note, Tag
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Import notes from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file_path', type=str)



    def handle(self, *args, **options):
        self.stdout.write("Завантаження Excel файлу...")
        wb = openpyxl.load_workbook(options['excel_file_path'])
        sheet = wb.active
        self.stdout.write("Обробка Excel файлу...")

        index = 1

        for row in sheet.iter_rows(min_row=2):
            self.stdout.write("Запуск...")

            # валідація даних рядків
            if not all([cell.value for cell in row[:5]]):
                self.stdout.write(self.style.WARNING(f"Skipping row {index} due to missing data"))
                continue

            title = row[0].value
            content = row[1].value
            tags = str(row[2].value).split(', ')  # Припускаємо, що теги розділені комами
            author_id = row[3].value
            editor_ids = str(row[4].value).split(', ')  # Припускаємо, що ID редакторів розділені комами

            try:
                author = User.objects.get(id=author_id)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User with ID {author_id} not found. Skipping note...'))
                continue

            # Створення або оновлення об'єкту Note
            note, created = Note.objects.update_or_create(
                id=100 + index,
                defaults={
                    'title': title,
                    'content': content,
                    'author': author
                }
            )

            # Очищуємо та встановлюємо нові теги
            note.tags.clear()
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(id=tag_name)
                note.tags.add(tag)

            # Очищуємо та встановлюємо нових редакторів
            note.editors.clear()
            for editor_id in editor_ids:
                editor = User.objects.get(id=editor_id)
                note.editors.add(editor)

            # видалення запису
            note_to_delete = Note.objects.filter(id=101).first()

            print(note_to_delete)
            # Виводимо повідомлення
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created note: {title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated note: {title}'))
            index += 1
