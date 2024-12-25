from django.urls import path
from knowledge import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.search_articles, name='search_articles'),
    path('vidannya/', views.search_vidannya, name='search_vidannya'),
    path('journals/', views.journals_view, name='journals'),
]
