from django.shortcuts import render
from knowledge.models import Article, KnowledgeField
from django.http import JsonResponse
from knowledge.models import Vidannya, GaluzNauki
from knowledge.models import Subject, Subtopic, JournalArticle
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Journal
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import FavoriteItem
from django.contrib.auth.decorators import login_required

@login_required
def toggle_favorite(request):
    item_type = request.GET.get("type")
    item_id = request.GET.get("id")

    if item_type == "journal":
        obj, created = FavoriteItem.objects.get_or_create(
            user=request.user,
            journal_article_id=item_id
        )
    elif item_type == "vidannya":
        obj, created = FavoriteItem.objects.get_or_create(
            user=request.user,
            vidannya_id=item_id
        )
    else:
        return JsonResponse({"status": "error"}, status=400)

    if not created:
        obj.delete()

    return JsonResponse({"status": "ok", "action": "added" if created else "removed"})



def home(request):
    reg_form = UserCreationForm()
    login_form = AuthenticationForm()
    return render(request, 'knowledge/home.html', {
        'reg_form': reg_form,
        'login_form': login_form
    })

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect(f"{reverse('home')}?register_error=1")
    return redirect('home')


from django.urls import reverse

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect(f"{reverse('home')}?login_error=1")
    return redirect('home')

from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect('home')
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


from .models import Vidannya, FavoriteItem, GaluzNauki

def search_vidannya(request):
    query = request.GET.get('q', '')
    field = request.GET.get('field', '')

    vidannya_qs = Vidannya.objects.all()

    if query:
        vidannya_qs = vidannya_qs.filter(title__icontains=query)
    if field:
        vidannya_qs = vidannya_qs.filter(galuz__name=field)

    # ДОБАВИ ЦЕ ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    favorite_vidannya_ids = []
    if request.user.is_authenticated:
        favorite_vidannya_ids = FavoriteItem.objects.filter(
            user=request.user,
            vidannya__isnull=False
        ).values_list('vidannya_id', flat=True)

    # пагінація (якщо є)
    from django.core.paginator import Paginator
    paginator = Paginator(vidannya_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'vidannya_list': page_obj,
        'page_obj': page_obj,
        'query': query,
        'field': field,
        'galuz': GaluzNauki.objects.all(),
        'favorite_vidannya_ids': list(favorite_vidannya_ids),  # ОБОВ’ЯЗКОВО
    }

    return render(request, 'knowledge/vidannya.html', context)








from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def journals_view(request):
    theme = request.GET.get("theme", "")
    subtopic = request.GET.get("subtopic", "")
    query = request.GET.get("q", "")

    journals = JournalArticle.objects.all()
    if theme:
        selected_subject = Subject.objects.filter(name=theme).first()
        if selected_subject:
            journals = journals.filter(subtopic__subject=selected_subject)
    if subtopic:
        journals = journals.filter(subtopic__name=subtopic)
    if query:
        journals = journals.filter(title__icontains=query) | journals.filter(author__icontains=query)

    paginator = Paginator(journals, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    subjects = Subject.objects.all()
    translated_subjects = [{"name": s.name, "name_uk": theme_translation_dict.get(s.name, s.name)} for s in subjects]

    selected_subject = Subject.objects.filter(name=theme).first() if theme else None
    subtopics = Subtopic.objects.filter(subject=selected_subject) if selected_subject else []
    translated_subtopics = [{"name": st.name, "name_uk": subtopic_translation_dict.get(st.name, st.name)} for st in subtopics]

    # Додати список обраних id для поточного користувача
    favorite_journal_ids = []
    if request.user.is_authenticated:
        favorite_journal_ids = list(
            request.user.favoriteitem_set.filter(journal_article__isnull=False).values_list('journal_article_id', flat=True)
        )

    context = {
        "journals": page_obj,
        "subjects": translated_subjects,
        "subtopics": translated_subtopics,
        "selected_theme": theme,
        "selected_subtopic": subtopic,
        "query": query,
        "favorite_journal_ids": favorite_journal_ids,
        "reg_form": UserCreationForm(),
        "login_form": AuthenticationForm(),
    }
    return render(request, "knowledge/journals.html", context)




# journals/views.py

class JournalListView(ListView):
    model = Journal
    template_name = 'knowledge/journal_list.html'  # укажите свой путь
    context_object_name = 'journals'
    paginate_by = 20  # например, пагинация на 20 записей

    def get_queryset(self):
        qs = super().get_queryset()

        # Получаем данные из GET-запроса
        search_query = self.request.GET.get('q', '')  # строка поиска (название)
        science_field_filter = self.request.GET.get('science', '')  # галузь науки
        specialty_filter = self.request.GET.get('specialty', '')    # спеціальність

        # Фильтр по названию
        if search_query:
            qs = qs.filter(title__icontains=search_query)

        # Фильтр по галузі науки
        if science_field_filter:
            qs = qs.filter(science_field__icontains=science_field_filter)

        # Фильтр по спеціальності
        if specialty_filter:
            qs = qs.filter(specialty__icontains=specialty_filter)

        return qs

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user
    favorite_journals = FavoriteItem.objects.filter(user=request.user, journal_article__isnull=False)

    favorite_vidannya = FavoriteItem.objects.filter(user=request.user, vidannya__isnull=False)


    return render(request, 'knowledge/profile.html', {
        'user': user,
        'favorite_journals': favorite_journals,
        'favorite_vidannya': favorite_vidannya,
    })

