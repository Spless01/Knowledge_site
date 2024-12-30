from django.urls import path
from knowledge import views
# journals/urls.py
from .views import JournalListView



urlpatterns = [
    path('', views.home, name='home'),
    path('journals/', views.journals_view, name='journals'),
    path('vidannya/', JournalListView.as_view(), name='journal_list'),
]
