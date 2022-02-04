from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
"""
?djoser library provides a set of Django Rest Framework 
?views to handle basic actions such as 
?registration, login, logout, password reset and account activation. 
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include('product.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)