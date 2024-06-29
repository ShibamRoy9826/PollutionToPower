from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from projects import views as projectViews

urlpatterns = [
    path('project/',projectViews.allProjects, name="allProjects")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
