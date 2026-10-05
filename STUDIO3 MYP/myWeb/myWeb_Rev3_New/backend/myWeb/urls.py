from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from members import views as member_views
from members.views import faq_view

def home(request):
    return render(request, 'members/index.html')  # ใช้ไฟล์เดิม

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
    path('', home, name='home'),
    path('faq/', faq_view, name='faq'),
]