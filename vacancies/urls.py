from django.urls import path, re_path
from vacancies import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="main"),
    path("vacancies/", views.ListVacanciesView.as_view(), name="vacancies"),
    #re_path(r"^vacancies/cat/(?P<specialty>\w+)/$", views.ListCategoryView.as_view(), name="category"),
    path("vacancies/cat/<str:pk>/", views.ListCategoryView.as_view(), name="category"),
    path("companies/<int:pk>", views.ListCompanyView.as_view(), name="company"),
    path("vacancies/<int:pk>", views.DetailVacancyView.as_view(), name="vacancy"),
    ]

handler404 = views.custom_handler404
handler500 = views.custom_handler500
