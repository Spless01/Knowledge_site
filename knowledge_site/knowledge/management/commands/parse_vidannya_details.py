
import requests
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db.utils import DataError
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from knowledge.models import Vidannya, Journal

class Command(BaseCommand):
    help = (
        "Парсит детальную информацию (Галузь науки, Спеціальності, ISSN) "
        "из ссылок Vidannya и записывает в Journal."
    )

    def add_arguments(self, parser):
        # Параметр, чтобы можно было регулировать кол-во потоков
        parser.add_argument(
            '--workers',
            type=int,
            default=10,
            help="Количество потоков для параллельного парсинга (по умолчанию 10)."
        )

    def handle(self, *args, **options):
        workers = options['workers']

        # Загружаем из Vidannya все, что нужно парсить
        vidannyas = Vidannya.objects.all()
        total_count = vidannyas.count()
        self.stdout.write(self.style.SUCCESS(
            f"Всего записей для парсинга: {total_count}"
        ))

        # ---------- Функция парсинга ОДНОЙ записи ----------
        def parse_one_vidannya(vid):
            """
            Парсит страницу vid.link, извлекает:
              - Галузь науки (из div[name="galuzNakazView"])
              - Спеціальності (из div[name="specilnostiView"])
              - ISSN (после <span class="viewText">ISSN</span>...)
              - Домашняя страница (если <a>Домашня сторінка</a>)
            Сохраняет/обновляет в Journal.
            Возвращает (vid, True, None) если успех, иначе (vid, False, reason).
            """
            if not vid.link:
                return (vid, False, "Нет ссылки (vid.link)")

            url = vid.link.strip()
            try:
                resp = requests.get(
                    url,
                    timeout=5,  # Уменьшенный таймаут для скорости
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/131.0.0.0 Safari/537.36"
                        )
                    }
                )
                resp.raise_for_status()
            except (requests.RequestException, requests.HTTPError) as e:
                return (vid, False, f"Ошибка при GET {url}: {e}")

            soup = BeautifulSoup(resp.text, "html.parser")

            # ---------------------- 1) Галузь науки ----------------------

            science_field = ""
            galuz_div = soup.find("div", {"name": "galuzNakazView"})
            if galuz_div:
                b_list = galuz_div.find_all("b")
                values = []
                for btag in b_list:
                    text = btag.get_text(strip=True)
                    # Если это строка вида "(27.04.2023)" - пропускаем
                    if re.match(r'^\(\d{2}\.\d{2}\.\d{4}\)$', text):
                        continue
                    # Иначе добавляем в список
                    values.append(text)
                if values:
                    science_field = ", ".join(values)

            # ---------------------- 2) Спеціальності ----------------------

            specialty = ""
            spec_div = soup.find("div", {"name": "specilnostiView"})
            if spec_div:
                b_list = spec_div.find_all("b")
                values = []
                for btag in b_list:
                    text = btag.get_text(strip=True)
                    # Снова пропускаем, если это дата вида (дд.мм.гггг)
                    if re.match(r'^\(\d{2}\.\d{2}\.\d{4}\)$', text):
                        continue
                    values.append(text)
                if values:
                    specialty = ", ".join(values)

            # ---------------------- 3) ISSN ----------------------

            issn_value = ""
            issn_label = soup.find("span", class_="viewText", string=re.compile(r"^ISSN"))
            if issn_label:
                next_b = issn_label.find_next("b")
                if next_b:
                    issn_value = next_b.get_text(strip=True)

            # ---------------------- 4) Домашняя страница ----------------------
            home_link = ""
            home_page_a = soup.find("a", string="Домашня сторінка")
            if home_page_a:
                home_link = home_page_a.get("href", "")

            # ---------------------- Сохраняем в Journal ----------------------
            try:
                obj, created = Journal.objects.update_or_create(
                    title=vid.title,  # ориентируемся на title в Vidannya
                    defaults={
                        "science_field": science_field,
                        "specialty": specialty,
                        "issn": issn_value,
                        # Если нашли "Домашня сторінка" - записываем, иначе остаётся исходная ссылка
                        "link": home_link if home_link else vid.link,
                    }
                )
                return (vid, True, None)
            except DataError as e:

                return (vid, False, f"DataError при сохранении: {e}")
            except Exception as e:
                return (vid, False, f"Ошибка при сохранении: {e}")

        # ---------- Запускаем параллельно ----------
        results = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_vid = {
                executor.submit(parse_one_vidannya, v): v
                for v in vidannyas
            }

            for future in tqdm(as_completed(future_to_vid), total=len(future_to_vid), desc="Парсим видання"):
                vid = future_to_vid[future]
                try:
                    vid_obj, success, err_msg = future.result()
                    if success:
                        self.stdout.write(self.style.SUCCESS(
                            f"[OK] [{vid_obj.id}] {vid_obj.title}"
                        ))
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"[SKIP] [{vid_obj.id}] {vid_obj.title}: {err_msg}"
                        ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"[ERROR] [{vid.id}] {vid.title}: {e}"
                    ))

        self.stdout.write(self.style.SUCCESS("Парсинг завершён!"))
