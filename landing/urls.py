from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from landing import views as landingView

urlpatterns = [
    path('',landingView.home, name="landingPage")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
