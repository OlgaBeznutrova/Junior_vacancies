from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from vacancies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vacancies.urls')),
    path('', include('accounts.urls')),
]

handler404 = views.custom_handler404

handler500 = views.custom_handler500

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # для media-файлов
    urlpatterns += staticfiles_urlpatterns()
