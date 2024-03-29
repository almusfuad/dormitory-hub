"""
URL configuration for dormitory_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import schema_view, swagger_ui_view


urlpatterns = [
    path('', swagger_ui_view, name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('user/', include('student.urls', namespace='student')),
    path('', include('dormitory.urls', namespace='dormitory')),
    path('transactions/', include('transaction.urls', namespace='transactions')),
    path('booking/', include('booking.urls', namespace='booking')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
