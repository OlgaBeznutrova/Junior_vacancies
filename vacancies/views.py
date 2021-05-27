from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from .forms import CompanyForm, VacancyForm, ApplicationForm
from .models import Specialty, Vacancy, Company


class HomePageView(TemplateView):
    template_name = "vacancies/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["specialties"] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context["companies"] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        return context


class AllVacancies(ListView):
    template_name = "vacancies/vacancies.html"
    context_object_name = "vacancies"
    queryset = Vacancy.objects.select_related("company", "specialty")
    extra_context = {"title": "Все вакансии"}


class VacanciesByCategory(ListView):
    model = Vacancy
    template_name = "vacancies/vacancies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = get_object_or_404(Specialty, code=self.kwargs["category_code"]).title
        context["vacancies"] = Vacancy.objects.filter(specialty__title=context["title"]).select_related("company",
                                                                                                        "specialty")
        return context


class VacanciesByCompany(ListView):
    model = Vacancy
    template_name = "vacancies/vacancies_by_company.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["pk"])
        context["vacancies"] = Vacancy.objects.filter(company__pk=self.kwargs["pk"]).select_related("company",
                                                                                                    "specialty")
        return context


class VacancyDetail(DetailView, FormMixin):
    model = Vacancy
    form_class = ApplicationForm

    def get_success_url(self):
        return reverse("application_send", kwargs={'pk': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.vacancy_id = self.kwargs['pk']
        form.save()  # сохраняем запись в бд сами, т.к. FormMixin и его родители этого не делают.
        return super().form_valid(form)


class ApplicationSend(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = "vacancies/application_send.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["vacancy_pk"] = self.kwargs["pk"]
        return context


class IfNoCompanyMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("login")

    def test_func(self):
        return not Company.objects.filter(owner=self.request.user).exists()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("company_update")


class LetsStart(IfNoCompanyMixin, TemplateView):
    template_name = "vacancies/lets_start.html"


class CreateCompany(IfNoCompanyMixin, CreateView):
    form_class = CompanyForm
    template_name = "vacancies/company_form.html"
    success_url = reverse_lazy("company_update")
    extra_context = {"title": "Создание компании"}

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f"Компания {form.instance.name} успешно создана!")
        return super().form_valid(form)


class IfCompanyIsMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("login")

    def test_func(self):
        return Company.objects.filter(owner=self.request.user).exists()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return redirect("lets_start")


class UpdateCompany(IfCompanyIsMixin, SuccessMessageMixin, UpdateView):
    form_class = CompanyForm
    template_name = "vacancies/company_form.html"
    success_url = reverse_lazy("company_update")
    success_message = "Информация о компании обновлена!"
    extra_context = {"title": "Обновление данных компании"}

    def get_object(self, queryset=None):
        return self.request.user.company


class MyVacanciesList(IfCompanyIsMixin, ListView):
    template_name = "vacancies/my_vacancies_list.html"

    def get_queryset(self):
        return Vacancy.objects.filter(company=self.request.user.company)


class CreateVacancy(IfCompanyIsMixin, CreateView):
    form_class = VacancyForm
    template_name = "vacancies/vacancy_form.html"
    extra_context = {"title": "Создание вакансии"}

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.success(self.request, f"Вакансия *{form.instance.title}* создана!")
        return super().form_valid(form)


class UpdateVacancy(IfCompanyIsMixin, UpdateView):
    form_class = VacancyForm
    template_name = "vacancies/vacancy_form.html"
    extra_context = {"title": "Обновление данных вакансии"}

    def get_object(self, queryset=None):
        return get_object_or_404(Vacancy, company=self.request.user.company, pk=self.kwargs["pk"])

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.success(self.request, f"Вакансия *{form.instance.title}* обновлена!")
        return super().form_valid(form)


def custom_handler404(request, exception):
    return HttpResponseNotFound("Ресурс не найден!")


def custom_handler500(request):
    return HttpResponseServerError("Ошибка сервера!")
