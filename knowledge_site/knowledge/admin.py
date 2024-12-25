from django.contrib import admin
from .models import KnowledgeField, Article
from .models import GaluzNauki, Vidannya
admin.site.register(KnowledgeField)
admin.site.register(Article)


@admin.register(GaluzNauki)
class GaluzNaukiAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Vidannya)
class VidannyaAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "galuz")
    search_fields = ("title",)
    list_filter = ("galuz",)
