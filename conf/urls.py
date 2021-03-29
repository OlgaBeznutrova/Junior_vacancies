from django.conf import settings
from django.conf.urls import include
from django.urls import path

from vacancies import views

urlpatterns = [
    path("", include("vacancies.urls")),
]

handler404 = views.custom_handler404

handler500 = views.custom_handler500

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
