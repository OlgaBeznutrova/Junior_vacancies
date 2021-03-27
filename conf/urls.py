from django.urls import path
from django.conf.urls import include

from vacancies import views

urlpatterns = [
    path("", include("vacancies.urls")),
]

handler404 = views.custom_handler404

handler500 = views.custom_handler500
