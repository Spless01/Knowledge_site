from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from knowledge.models import Vidannya, GaluzNauki


class Command(BaseCommand):
    help = "Парсинг данных по галузям науки и запись в базу данных"

    def handle(self, *args, **kwargs):
        base_url = "https://nfv.ukrintei.ua/search"
        view_base_url = "https://nfv.ukrintei.ua/view/"
        galuz_options = [
            "архітектура", "біологічні", "ветеринарні", "військові", "географічні", "геологічні",
            "державне управління", "економічні", "історичні", "культурологія", "медичні",
            "мистецтвознавство", "педагогічні", "політичні", "психологічні", "соціальні комунікації",
            "соціологічні", "сільськогосподарські", "технічні", "фармацевтичні",
            "фізико-математичні", "фізичне виховання і спорт", "філологічні", "філософські",
            "хімічні", "юридичні"
        ]

        for galuz in galuz_options:
            self.stdout.write(f"Парсим галузь: {galuz}")
            page = 1

            while True:
                params = {
                    "sortOrder": "title",
                    "galuzSearch[]": galuz,
                    "page": page
                }
                response = requests.get(base_url, params=params)
                soup = BeautifulSoup(response.text, "html.parser")

                # Найти все блоки выданий
                search_block_elements = soup.find_all("div", attrs={"name": "searchBlockElement"})

                if not search_block_elements:
                    self.stdout.write(f"Нет данных на странице {page} для галузи {galuz}")
                    break

                for item in search_block_elements:
                    try:
                        # Название выдания
                        title_tag = item.find("span", attrs={"name": "nameSearchMain"})
                        title = title_tag.a.text.strip() if title_tag and title_tag.a else "Не указано"

                        # Ссылка на выдание
                        link_tag = title_tag.a if title_tag and title_tag.a else None
                        if link_tag:
                            raw_link = link_tag['href']
                            link = f"{view_base_url}{raw_link}".replace('//view/view/', '/view/').replace('/view/view/', '/view/')
                        else:
                            link = None

                        # Вывод ссылки для диагностики
                        print(f"Название: {title}, Ссылка: {link}")

                        # Запись в базу данных
                        galuz_obj, _ = GaluzNauki.objects.get_or_create(name=galuz)
                        Vidannya.objects.create(
                            title=title,
                            galuz=galuz_obj,
                            link=link
                        )

                    except Exception as e:
                        self.stderr.write(f"Ошибка при обработке элемента: {e}")

                self.stdout.write(f"Данные успешно спарсены со страницы {page} для галузи {galuz}")
                page += 1

        self.stdout.write("Парсинг завершён.")
