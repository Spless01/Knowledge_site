from django.db import models

class KnowledgeField(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=2500)  # Название статьи
    link = models.URLField(max_length=2500, null=True, blank=True, default="Ссылка отсутствует")  # Ссылка
    doi = models.CharField(max_length=2500, null=True, blank=True)  # DOI
    author = models.CharField(max_length=2500, null=True, blank=True, default="Автор отсутствует")
    field = models.ForeignKey(KnowledgeField, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title

class GaluzNauki(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Назва галузі науки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Галузь науки"
        verbose_name_plural = "Галузі науки"


class Vidannya(models.Model):
    title = models.CharField(max_length=255)
    galuz = models.ForeignKey(GaluzNauki, on_delete=models.CASCADE)
    link = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видання"
        verbose_name_plural = "Видання"

class Subject(models.Model):  # Тема
    name = models.CharField(max_length=255, unique=True)  # Название темы (англ.)
    name_uk = models.CharField(max_length=255, unique=True)  # Название темы (укр.)
    link = models.URLField()  # Ссылка на тему

    def __str__(self):
        return self.name_uk

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Subtopic(models.Model):  # Подтема
    subject = models.ForeignKey(Subject, related_name="subtopics", on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)  # Название подтемы (англ.)
    name_uk = models.CharField(max_length=255)  # Название подтемы (укр.)
    link = models.URLField()  # Ссылка на подтему

    def __str__(self):
        return self.name_uk

    class Meta:
        verbose_name = "Подтема"
        verbose_name_plural = "Подтемы"


class JournalArticle(models.Model):  # Статья
    subtopic = models.ForeignKey(Subtopic, related_name="articles", on_delete=models.CASCADE)
    title = models.CharField(max_length=3000)  # Название статьи
    author = models.CharField(max_length=255, null=True, blank=True)  # Автор статьи
    article_link = models.URLField()  # Ссылка на статью
    download_link = models.URLField(null=True, blank=True)  # Ссылка на скачивание

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Журнал"
        verbose_name_plural = "Журналы"
