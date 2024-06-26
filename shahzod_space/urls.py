# shahzod_space/urls.py
from django.contrib import admin
from django.urls import path, include
from shahzodspace import views  
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('shahzodspace.urls')),  
    path('', views.home, name='home'),  
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


