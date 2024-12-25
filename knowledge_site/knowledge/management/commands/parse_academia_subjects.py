import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from knowledge.models import Subject, Subtopic, JournalArticle
import time
# Локальный словарь переводов
theme_translation_dict = {
    "History": "Історія",
    "Engineering": "Інженерія",
    "Economics": "Економіка",
    "Psychology": "Психологія",
    "Physics": "Фізика",
    "Anthropology": "Антропологія",
    "Philosophy": "Філософія",
    "Chemistry": "Хімія",
    "Earth Sciences": "Науки про Землю",
    "Computer Science": "Комп'ютерні науки",
    "Mathematics": "Математика",
    "Literature": "Література",
    "Law": "Право",
    "Health Sciences": "Медичні науки",
    "Biology": "Біологія",
    "Theology": "Теологія"
}

subtopic_translation_dict = {
    "Medieval History": "Середньовічна історія",
    "Ancient History": "Стародавня історія",
    "Cultural History": "Культурна історія",
    "Urban History": "Історія міст",
    "Ancient Greek History": "Історія Стародавньої Греції",
    "Military History": "Воєнна історія",
    "Electrical And Electronic Engineering": "Електротехніка та електроніка",
    "Materials Engineering": "Матеріалознавство",
    "Biomedical Engineering": "Біомедична інженерія",
    "Environmental Engineering": "Екологічна інженерія",
    "Mechanical Engineering": "Машинобудування",
    "Chemical Engineering": "Хімічна інженерія",
    "Civil Engineering": "Будівельна інженерія",
    "Manufacturing Engineering": "Інженерія виробництва",
    "Applied Economics": "Прикладна економіка",
    "Economic Development": "Економічний розвиток",
    "Economic History": "Історія економіки",
    "Macroeconomics": "Макроекономіка",
    "Econometrics": "Економетрика",
    "Development Economics": "Економіка розвитку",
    "Agricultural Economics": "Сільськогосподарська економіка",
    "Economic policy": "Економічна політика",
    "Social Psychology": "Соціальна психологія",
    "Cognitive Psychology": "Когнітивна психологія",
    "Educational Psychology": "Психологія освіти",
    "Child Psychology": "Дитяча психологія",
    "Clinical Psychology": "Клінічна психологія",
    "Developmental Psychology": "Психологія розвитку",
    "Health Psychology": "Психологія здоров’я",
    "Abnormal Psychology": "Аномальна психологія",
    "Quantum Physics": "Квантова фізика",
    "High Energy Physics": "Фізика високих енергій",
    "Particle Physics": "Фізика частинок",
    "Aerodynamics": "Аеродинаміка",
    "Condensed Matter Physics": "Фізика конденсованих середовищ",
    "Astrophysics": "Астрофізика",
    "Molecular Physics": "Молекулярна фізика",
    "Nuclear Physics": "Ядерна фізика",
    "Social and Cultural Anthropology": "Соціальна та культурна антропологія",
    "Medical Anthropology": "Медична антропологія",
    "Anthropology of Religion": "Антропологія релігії",
    "Visual Anthropology": "Візуальна антропологія",
    "Physical Anthropology": "Фізична антропологія",
    "Forensic Anthropology": "Судова антропологія",
    "Linguistic Anthropology": "Лінгвістична антропологія",
    "Political Anthropology": "Політична антропологія",
    "Ethics": "Етика",
    "Political Philosophy": "Політична філософія",
    "Bioethics": "Біоетика",
    "Moral Philosophy": "Моральна філософія",
    "Medical Ethics": "Медична етика",
    "Philosophy Of Religion": "Філософія релігії",
    "Philosophy Of Language": "Філософія мови",
    "Philosophy of Science": "Філософія науки",
    "Analytical Chemistry": "Аналітична хімія",
    "Electrochemistry": "Електрохімія",
    "Physical Chemistry": "Фізична хімія",
    "Chemical Synthesis": "Хімічний синтез",
    "Inorganic Chemistry": "Неорганічна хімія",
    "Materials Chemistry": "Хімія матеріалів",
    "Geochemistry": "Геохімія",
    "Quantum Chemistry": "Квантова хімія",
    "Environmental Science": "Наука про довкілля",
    "Climate Change": "Зміна клімату",
    "Atmospheric sciences": "Атмосферні науки",
    "Hydrology": "Гідрологія",
    "Geology": "Геологія",
    "Oceanography": "Океанографія",
    "Environmental Sustainability": "Екологічна стійкість",
    "Environmental Pollution": "Забруднення довкілля",
    "Machine Learning": "Машинне навчання",
    "Cryptography": "Криптографія",
    "Logic Programming": "Логічне програмування",
    "Natural Language Processing": "Обробка природної мови",
    "Computational Complexity": "Обчислювальна складність",
    "Programming Languages": "Мови програмування",
    "Functional Programming": "Функціональне програмування",
    "Artificial Intelligence": "Штучний інтелект",
    "Statistics": "Статистика",
    "Game Theory": "Теорія ігор",
    "Algebraic Geometry": "Алгебраїчна геометрія",
    "Algebraic Topology": "Алгебраїчна топологія",
    "Numerical Analysis": "Чисельний аналіз",
    "Combinatorics": "Комбінаторика",
    "Linear Algebra": "Лінійна алгебра",
    "Applied Mathematics": "Прикладна математика",
    "Comparative Literature": "Порівняльна література",
    "Literary Theory": "Літературознавча теорія",
    "Literary Criticism": "Літературна критика",
    "Postcolonial Literature": "Постколоніальна література",
    "American Literature": "Американська література",
    "English Literature": "Англійська література",
    "Medieval Literature": "Середньовічна література",
    "Contemporary Literature": "Сучасна література",
    "Human Rights": "Права людини",
    "Criminal Justice": "Кримінальне правосуддя",
    "Criminal Law": "Кримінальне право",
    "Legal Theory": "Правова теорія",
    "International Law": "Міжнародне право",
    "Constitutional Law": "Конституційне право",
    "Legal History": "Історія права",
    "Environmental Law": "Екологічне право",
    "Emergency Medicine": "Невідкладна медицина",
    "Cardiology": "Кардіологія",
    "Infectious Diseases": "Інфекційні хвороби",
    "Clinical Allergy and Immunology": "Клінічна алергологія та імунологія",
    "Public Health": "Громадське здоров’я",
    "Neurology": "Неврологія",
    "Internal Medicine": "Внутрішня медицина",
    "Medicine": "Медицина",
    "Microbiology": "Мікробіологія",
    "Evolutionary Biology": "Еволюційна біологія",
    "Biochemistry": "Біохімія",
    "Biodiversity": "Біорізноманіття",
    "Plant Biology": "Біологія рослин",
    "Molecular Biology": "Молекулярна біологія",
    "Bioinformatics": "Біоінформатика",
    "Cell Biology": "Клітинна біологія",
    "Religious Studies": "Релігієзнавство",
    "Systematic Theology": "Систематична теологія",
    "Catholic Theology": "Католицька теологія",
    "Biblical Theology": "Біблійна теологія",
    "History of Religion": "Історія релігії",
    "Ancient myth and religion": "Стародавні міфи та релігія",
    "Comparative Religion": "Порівняльне релігієзнавство"

}

base_url = "https://www.academia.edu"

class Command(BaseCommand):
    help = "Парсинг тем, подтем и статей с сайта Academia.edu"

    def handle(self, *args, **kwargs):
        self.parse_academia_articles()

    def parse_academia_articles(self):
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Парсинг тем
        main_subjects = soup.find_all("div", class_="research-interest-section-container")

        for subject in main_subjects:
            subject_name = subject.find("h3", class_="primary-interest-title").get_text(strip=True)
            subject_name_uk = theme_translation_dict.get(subject_name, subject_name)
            print(f"Тема: {subject_name} ({subject_name_uk})")

            # Сохранение темы в БД
            subject_obj, _ = Subject.objects.get_or_create(
                name=subject_name,
                defaults={"name_uk": subject_name_uk}
            )

            subtopics_container = subject.find("div", class_="research-interest-list-container")
            if subtopics_container:
                subtopics = subtopics_container.find_all("a", class_="research-interest-list-item-content")
                for subtopic in subtopics:
                    subtopic_name = subtopic.find("div", class_="research-interest-list-item-name").get_text(strip=True)
                    subtopic_name_uk = subtopic_translation_dict.get(subtopic_name, subtopic_name)
                    subtopic_link = subtopic.get("href")
                    full_subtopic_link = f"{base_url}{subtopic_link}" if subtopic_link.startswith("/") else subtopic_link

                    print(f"  Подтема: {subtopic_name} ({subtopic_name_uk}) | Ссылка: {full_subtopic_link}")

                    # Сохранение подтемы в БД
                    subtopic_obj, _ = Subtopic.objects.get_or_create(
                        subject=subject_obj,
                        name=subtopic_name,
                        defaults={"name_uk": subtopic_name_uk, "link": full_subtopic_link}
                    )

                    # Парсинг статей из подтемы
                    self.parse_articles_from_subtopic(subtopic_obj, full_subtopic_link)

    def parse_articles_from_subtopic(self, subtopic_obj, subtopic_url):
        after_param = None
        page_count = 0

        while True:
            # Формируем URL для текущей страницы
            page_url = f"{subtopic_url}?after={after_param}" if after_param else subtopic_url
            print(f"Парсинг страницы: {page_url}")

            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Находим статьи на текущей странице
            articles = soup.find_all("div", class_="u-borderColorGrayLighter")
            if not articles:
                print("Статьи на текущей странице не найдены.")
                break

            # Обработка статей
            for article in articles:
                try:
                    title_tag = article.find("a", class_="u-tcGrayDarkest")
                    title = title_tag.get_text(strip=True) if title_tag else "Название отсутствует"
                    author_tag = article.find("span", class_="InlineList-item-text")
                    author = author_tag.get_text(strip=True).replace("by", "").strip() if author_tag else "Автор отсутствует"
                    download_button = article.find("a", class_="Button--inverseGreen")
                    download_link = f"{base_url}{download_button['href']}" if download_button and download_button['href'].startswith("/") else download_button['href']
                    article_link = f"{base_url}{title_tag['href']}" if title_tag and title_tag['href'].startswith("/") else title_tag['href']

                    print(f"    Название: {title}")
                    print(f"    Автор: {author}")
                    print(f"    Ссылка на журнал: {article_link}")
                    print(f"    Ссылка на скачивание: {download_link}")

                    # Сохранение статьи в БД
                    JournalArticle.objects.get_or_create(
                        subtopic=subtopic_obj,
                        title=title,
                        defaults={
                            "author": author,
                            "article_link": article_link,
                            "download_link": download_link
                        }
                    )
                except Exception as e:
                    print(f"Ошибка при обработке статьи: {e}")

            page_count += 1
            print(f"  Обработана страница {page_count}")

            # Проверяем наличие кнопки "Next"
            next_page = soup.find("a", rel="next")
            if not next_page:
                print("Дополнительных страниц не найдено.")
                break

            # Обновляем значение параметра "after" из ссылки "Next"
            after_param = next_page['href'].split('after=')[1]
            time.sleep(2)  # Задержка между запросами для предотвращения блокировки

        print(f"Для подтемы '{subtopic_obj.name_uk}' было спаршено {page_count} страниц.")


