from django.urls import path, include
from Manager.views import *
from Manager.admin import admin_site
from .yasg import urlpatterns as url


urlpatterns = [
    path('admin/', admin_site.urls),
    path('users/', include('Manager.urls')),
]

urlpatterns += url
