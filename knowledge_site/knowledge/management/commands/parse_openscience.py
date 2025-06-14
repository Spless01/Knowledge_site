import time
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from knowledge.models import Journal
from tqdm import tqdm

class Command(BaseCommand):
    help = "Парсинг даних с https://openscience.in.ua/ab-journals та зберігаємо у БД."

    def handle(self, *args, **options):
        url = "https://openscience.in.ua/ab-journals"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            )
        }

        # Чекаємо 3 сек перед запитом
        time.sleep(1)

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Не вдалося відкрити {url} (код {response.status_code})"))
            return

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", attrs={"id": "tablepress-28"})
        if not table:
            self.stdout.write(self.style.ERROR("Таблиця с id='tablepress-28' не знайдена."))
            return

        rows = table.find("tbody").find_all("tr", recursive=False)
        total = len(rows)

        created_count = 0
        updated_count = 0

        # Використовуємо tqdm, щоб відобразити прогресс проходу по рядкам
        for row in tqdm(rows, desc="Парсинг строк", total=total):
            science_field_td = row.find("td", class_="column-2")
            specialty_td = row.find("td", class_="column-3")
            title_td = row.find("td", class_="column-4")
            issn_td = row.find("td", class_="column-5")

            if not (science_field_td and specialty_td and title_td and issn_td):
                continue

            science_field = science_field_td.get_text(strip=True)
            specialty = specialty_td.get_text(strip=True)

            link_a = title_td.find("a")
            if link_a:
                title = link_a.get_text(strip=True)
                link = link_a.get("href", "")
            else:
                title = title_td.get_text(strip=True)
                link = ""

            issn = issn_td.get_text(separator=" ", strip=True)

            obj, created = Journal.objects.update_or_create(
                title=title,
                defaults={
                    "science_field": science_field,
                    "specialty": specialty,
                    "link": link,
                    "issn": issn,
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nВиконано! Додано {created_count}, Оновлено {updated_count}."
        ))
