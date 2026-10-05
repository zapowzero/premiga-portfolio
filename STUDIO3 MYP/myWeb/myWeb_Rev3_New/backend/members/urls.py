from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import faq_view

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('search/', views.member_search, name='member_search'),
    path('add/', views.member_add, name='member_add'),
    path('edit/<int:pk>/', views.member_edit, name='member_edit'),
    path('delete/<int:pk>/', views.member_delete, name='member_delete'),
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.event_add, name='event_add'),
    path('events/edit/<int:pk>/', views.event_edit, name='event_edit'),
    path('events/delete/<int:pk>/', views.event_delete, name='event_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='members/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('faq/', faq_view, name='faq'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
]