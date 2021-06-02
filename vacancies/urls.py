from django.urls import path

from vacancies import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home_page"),
    path("vacancies/", views.AllVacancies.as_view(), name="vacancies"),
    path("vacancies/cat/<str:category_code>/", views.VacanciesByCategory.as_view(), name="vacancies_by_category"),
    path("companies/<int:pk>/", views.VacanciesByCompany.as_view(), name="vacancies_by_company"),
    path("vacancies/<int:pk>/send/", views.ApplicationSend.as_view(), name="application_send"),
    path("vacancies/<int:pk>/", views.VacancyDetail.as_view(), name="vacancy_detail"),
    path("mycompany/letsstart/", views.LetsStartCompany.as_view(), name="lets_start_company"),
    path("mycompany/create/", views.CreateCompany.as_view(), name="company_create"),
    path("mycompany/", views.UpdateCompany.as_view(), name="company_update"),
    path("mycompany/vacancies/", views.MyVacanciesList.as_view(), name="my_vacancies"),
    path("mycompany/vacancies/create/", views.CreateVacancy.as_view(), name="vacancy_create"),
    path("mycompany/vacancies/<int:pk>/", views.UpdateVacancy.as_view(), name="vacancy_update"),
    path("myresume/letsstart/", views.LetsStartResume.as_view(), name="lets_start_resume"),
    path("myresume/create/", views.CreateResume.as_view(), name="resume_create"),
    path("myresume/", views.UpdateResume.as_view(), name="resume_update"),
    path("search/", views.Search.as_view(), name="search"),
]
