from django.urls import path
from knowledge import views
from django.contrib.auth import views as auth_views
# journals/urls.py
from .views import JournalListView
from django.contrib.auth.decorators import login_required
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('journals/', views.journals_view, name='journals'),
    path('vidannya/', views.search_vidannya, name='vidannya_list'),
    path('profile/', login_required(views.profile_view), name='profile'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),


]
