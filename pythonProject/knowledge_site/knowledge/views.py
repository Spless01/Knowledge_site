from django.shortcuts import render
from knowledge.models import Article, KnowledgeField
from django.http import JsonResponse
from knowledge.models import Vidannya, GaluzNauki
from knowledge.models import Subject, Subtopic, JournalArticle
from django.core.paginator import Paginator

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
    "Comparative Religion": "Порівняльне релігієзнавство",
    "Medieval Theology": "Середньовічна теологія",
    "Early Modern History": "Рання нова історія",
    "Roman History": "Римська історія"

}



def home(request):
    return render(request, 'knowledge/home.html')


def search_articles(request):
    field_id = request.GET.get("field", "")
    query = request.GET.get("query", "")

    print(f"ID из формы: {field_id}")
    # Получаем список всех галузей знань
    fields = KnowledgeField.objects.all()

    # Начальный запрос ко всем статьям
    articles = Article.objects.all()

    # Фильтрация по выбранной галузі знань
    if field_id:
        articles = articles.filter(field_id=field_id)

    # Фильтрация по названию статьи
    if query:
        articles = articles.filter(title__icontains=query)

    # Пагинация
    paginator = Paginator(articles, 10)  # 10 статей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Отправка данных в шаблон
    return render(request, "knowledge/search.html", {
        "fields": fields,
        "articles": page_obj,
        "selected_field": field_id,
        "query": query
    })


def search_vidannya(request):
    # Получаем параметры фильтрации
    field = request.GET.get("field", "")
    query = request.GET.get("q", "")

    # Фильтрация по области науки и поисковому запросу
    vidannya_list = Vidannya.objects.all()
    if field:
        vidannya_list = vidannya_list.filter(galuz__name=field)
    if query:
        vidannya_list = vidannya_list.filter(name__icontains=query)

    # Пагинация (10 записей на странице)
    paginator = Paginator(vidannya_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Все области наук для фильтрации
    galuz = GaluzNauki.objects.all()

    context = {
        "vidannya_list": page_obj,
        "galuz": galuz,
        "field": field,
        "query": query,
        "paginator": paginator,
        "page_obj": page_obj,
    }
    return render(request, "knowledge/vidannya.html", context)






def journals_view(request):
    theme = request.GET.get("theme", "")
    subtopic = request.GET.get("subtopic", "")
    query = request.GET.get("q", "")

    # Фильтрация статей
    journals = JournalArticle.objects.all()
    if theme:
        selected_subject = Subject.objects.filter(name=theme).first()
        if selected_subject:
            journals = journals.filter(subtopic__subject=selected_subject)
    if subtopic:
        journals = journals.filter(subtopic__name=subtopic)
    if query:
        journals = journals.filter(title__icontains=query) | journals.filter(author__icontains=query)

    # Пагинация
    paginator = Paginator(journals, 30)  # 30 статей на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Получение списка тем и подтем
    subjects = Subject.objects.all()
    translated_subjects = [{"name": s.name, "name_uk": theme_translation_dict.get(s.name, s.name)} for s in subjects]

    selected_subject = Subject.objects.filter(name=theme).first() if theme else None
    subtopics = Subtopic.objects.filter(subject=selected_subject) if selected_subject else []
    translated_subtopics = [{"name": st.name, "name_uk": subtopic_translation_dict.get(st.name, st.name)} for st in subtopics]

    context = {
        "journals": page_obj,
        "subjects": translated_subjects,
        "subtopics": translated_subtopics,
        "selected_theme": theme,
        "selected_subtopic": subtopic,
        "query": query,
    }
    return render(request, "knowledge/journals.html", context)


