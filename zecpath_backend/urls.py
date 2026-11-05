
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),

    path(
        'api/candidates/',
        include('apps.candidates.urls')
    ),

    path(
        'api/employers/',
        include('apps.employers.urls')
    ),
]
