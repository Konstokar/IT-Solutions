from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dds.urls')),
    path('', RedirectView.as_view(url='/', permanent=True)),
]