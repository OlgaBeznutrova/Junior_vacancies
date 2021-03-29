from django.urls import path

from vacancies import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="main"),
    path("vacancies/", views.ListVacanciesView.as_view(), name="vacancies"),
    path("vacancies/cat/<str:pk>/", views.CategoryView.as_view(), name="category"),
    path("companies/<int:pk>", views.CompanyView.as_view(), name="company"),
    path("vacancies/<int:pk>", views.DetailVacancyView.as_view(), name="vacancy"),

]
