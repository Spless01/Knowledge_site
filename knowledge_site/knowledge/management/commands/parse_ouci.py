import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://ouci.dntb.gov.ua/?discipline={}&p={}"  # Исправили page на p


def fetch_articles_for_discipline(discipline_code, discipline_name, max_pages=100):
    """Собирает статьи для одной дисциплины по страницам."""
    articles = []
    page = 1

    while page <= max_pages:
        url = BASE_URL.format(discipline_code, page)  # Используем корректный параметр p
        print(f"Запрос к странице: {url}")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"[Ошибка] Страница {page} вернула статус {response.status_code}.")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Получаем блоки статей
        results = soup.find_all('div', class_='result-section')
        if not results:
            print("Статьи на странице отсутствуют. Завершаем парсинг.")
            break

        for idx, result in enumerate(results):
            try:
                # Заголовок и ссылка
                title_tag = result.find('p', class_='result-title').find('a')
                title = title_tag.get_text(strip=True) if title_tag else "Без названия"
                link = "https://ouci.dntb.gov.ua" + title_tag[
                    'href'] if title_tag and 'href' in title_tag.attrs else "Ссылка отсутствует"

                # Автор
                author_tag = result.find('p', class_='text-muted text-small one-line')
                author = author_tag.get_text(strip=True) if author_tag else "Автор отсутствует"

                # DOI
                doi_tag = result.find('a', href=lambda x: x and 'doi.org' in x)
                doi_link = doi_tag['href'] if doi_tag else "DOI отсутствует"

                articles.append({
                    'Название статьи': title,
                    'Ссылка': link,
                    'DOI': doi_link,
                    'Автор': author
                })

            except Exception as e:
                print(f"Ошибка обработки статьи: {e}")

        print(f"Страница {page} обработана для дисциплины {discipline_name}.")
        page += 1  # Переход на следующую страницу

    # Сохранение в Excel
    if articles:
        safe_name = discipline_name.replace("/", "_").replace(" ", "_")
        file_name = f"{safe_name}_100pages.xlsx"
        df = pd.DataFrame(articles)
        df.to_excel(file_name, index=False)
        print(f"Файл {file_name} сохранен с {len(articles)} статьями.")
    else:
        print(f"Нет данных для дисциплины {discipline_name}.")


def main():
    disciplines = {
        "01": "Освіта/Педагогіка",
        "02": "Культура і мистецтво",
        "03": "Гуманітарні науки",
        "04": "Богослов’я",
        "05": "Соціальні та поведінкові науки",
        "06": "Журналістика",
        "07": "Управління та адміністрування",
        "08": "Право",
        "09": "Біологія",
        "10": "Природничі науки",
        "11": "Математика та статистика",
        "12": "Інформаційні технології",
        "13": "Механічна інженерія",
        "14": "Електрична інженерія",
        "15": "Автоматизація та приладобудування",
        "16": "Хімічна та біоінженерія",
        "17": "Електроніка та телекомунікації",
        "18": "Виробництво та технології",
        "19": "Архітектура та будівництво",
        "20": "Аграрні науки та продовольство",
        "21": "Ветеринарна медицина",
        "22": "Охорона здоров’я",
        "23": "Соціальна робота",
        "24": "Сфера обслуговування",
        "25": "Воєнні науки, національна безпека, безпека державного кордону",
        "26": "Цивільна безпека",
        "27": "Транспорт",
        "28": "Публічне управління та адміністрування",
        "29": "Міжнародні відносини",
    }

    for code, name in disciplines.items():
        print(f"\nСбор статей для дисциплины: {name}")
        fetch_articles_for_discipline(code, name, max_pages=100)


if __name__ == "__main__":
    main()
