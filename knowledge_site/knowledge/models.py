from django.db import models
from django.contrib.auth.models import User

class KnowledgeField(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=2500)  # Название статті
    link = models.URLField(max_length=2500, null=True, blank=True, default="Посилання відсутнє")  # Посилання
    doi = models.CharField(max_length=2500, null=True, blank=True)  # DOI
    author = models.CharField(max_length=2500, null=True, blank=True, default="Автор відсутній")
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
    name = models.CharField(max_length=255, unique=True)  # Назва теми (англ.)
    name_uk = models.CharField(max_length=255, unique=True)  # Назва теми (укр.)
    link = models.URLField()  # Посилання на тему

    def __str__(self):
        return self.name_uk

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Теми"

class Subtopic(models.Model):  # Підтема
    subject = models.ForeignKey(Subject, related_name="subtopics", on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)  # Назва підтеми (англ.)
    name_uk = models.CharField(max_length=255)  # Назва підтеми (укр.)
    link = models.URLField()  # Посилання на підтему

    def __str__(self):
        return self.name_uk

    class Meta:
        verbose_name = "Підтема"
        verbose_name_plural = "Підтеми"

class JournalArticle(models.Model):  # Стаття
    subtopic = models.ForeignKey(Subtopic, related_name="articles", on_delete=models.CASCADE)
    title = models.CharField(max_length=3000)  # Назва статті
    author = models.CharField(max_length=255, null=True, blank=True)  # Автор статті
    article_link = models.URLField()  # Посилання на статтю
    download_link = models.URLField(null=True, blank=True)  # Посилання на завантаження


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Журнал"
        verbose_name_plural = "Журнали"

class Journal(models.Model):
    science_field = models.CharField(max_length=2550, blank=True)   # Галузь науки
    specialty = models.CharField(max_length=2550, blank=True)       # Спеціальність
    title = models.CharField(max_length=1000)                       # Назва видання
    link = models.URLField(blank=True, null=True)                  # Посилання
    issn = models.CharField(max_length=1000, blank=True)            # ISSN/eISSN


    def __str__(self):
        return self.title



class FavoriteItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    journal_article = models.ForeignKey('JournalArticle', on_delete=models.CASCADE, null=True, blank=True)
    vidannya = models.ForeignKey('Vidannya', on_delete=models.CASCADE, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.journal_article and not self.vidannya:
            raise ValidationError("Потрібно обрати або журнал, або видання.")
        if self.journal_article and self.vidannya:
            raise ValidationError("Можна зберігати або журнал, або видання, але не обидва.")

    def __str__(self):
        if self.journal_article:
            return f"{self.user.username} - Журнал: {self.journal_article.title}"
        elif self.vidannya:
            return f"{self.user.username} - Видання: {self.vidannya.title}"
        return f"{self.user.username} - Обране (порожнє)"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "journal_article"], name="unique_favorite_journal"),
            models.UniqueConstraint(fields=["user", "vidannya"], name="unique_favorite_vidannya"),
        ]




