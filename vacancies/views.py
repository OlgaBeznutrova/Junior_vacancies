from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from .models import Specialty, Vacancy, Company


class HomePageView(TemplateView):
    template_name = "vacancies/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["specialties"] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context["companies"] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        return context


class ListVacanciesView(ListView):
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super(ListVacanciesView, self).get_context_data(**kwargs)
        context["title"] = "Все вакансии"
        return context


class ListCategoryView(ListView):
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super(ListCategoryView, self).get_context_data(**kwargs)
        context["title"] = get_object_or_404(Specialty, code=self.kwargs["pk"]).title
        context["object_list"] = Vacancy.objects.filter(specialty__title=context["title"])
        return context


class ListCompanyView(ListView):
    model = Vacancy
    template_name = "vacancies/company_list.html"

    def get_context_data(self, **kwargs):
        context = super(ListCompanyView, self).get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, id=self.kwargs["pk"])
        context["object_list"] = Vacancy.objects.filter(company__id=self.kwargs["pk"])
        return context


class DetailVacancyView(DetailView):
    model = Vacancy


def custom_handler404(request, exception):
    return HttpResponseNotFound("Ресурс не найден!")


def custom_handler500(request):
    return HttpResponseServerError("Ошибка сервера!")
