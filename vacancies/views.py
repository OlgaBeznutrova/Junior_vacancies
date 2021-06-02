from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, F, Q
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from .forms import CompanyForm, VacancyForm, ApplicationForm, ResumeForm
from .models import Specialty, Vacancy, Company, Resume, Application


class HomePageView(TemplateView):
    template_name = "vacancies/home_page.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["specialties"] = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        context["companies"] = Company.objects.annotate(vacancies_count=Count('vacancies'))
        return context


class AllVacancies(ListView):
    template_name = "vacancies/for_all_vacancies.html"
    context_object_name = "vacancies"
    queryset = Vacancy.objects.select_related("company", "specialty")
    paginate_by = 5
    extra_context = {"title": "Все вакансии", "count_vacancies": len(queryset)}


class VacanciesByCategory(ListView):
    template_name = "vacancies/for_all_vacancies.html"
    context_object_name = "vacancies"
    paginate_by = 5

    def get_queryset(self):
        return Vacancy.objects.filter(specialty__code=self.kwargs["category_code"]).select_related("company",
                                                                                                   "specialty")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = get_object_or_404(Specialty, code=self.kwargs["category_code"])
        context["count_vacancies"] = self.object_list.count
        return context


class VacanciesByCompany(ListView):
    template_name = "vacancies/for_vacancies_by_company.html"
    context_object_name = "vacancies"
    paginate_by = 5

    def get_queryset(self):
        return Vacancy.objects.filter(company_id=self.kwargs["pk"]).select_related("company", "specialty")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = get_object_or_404(Company, pk=self.kwargs["pk"])
        context["count_vacancies"] = self.object_list.count
        return context


class VacancyDetail(DetailView, FormMixin):
    model = Vacancy
    form_class = ApplicationForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F("views") + 1
        self.object.save()
        return context

    def get_success_url(self):
        return reverse("application_send", kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.vacancy_id = self.kwargs['pk']
        form.save()  # сохраняем запись в бд сами, т.к. FormMixin и его родители этого не делают.
        return super().form_valid(form)


class ApplicationSend(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = "vacancies/application_send.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancy_pk"] = self.kwargs["pk"]
        return context


class IfAlreadyCompanyIs(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("login")

    def test_func(self):
        return not Company.objects.filter(owner=self.request.user).exists()

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return super().handle_no_permission()
        return redirect("company_update")


class LetsStartCompany(IfAlreadyCompanyIs, TemplateView):
    template_name = "vacancies/lets_start_company.html"


class CreateCompany(IfAlreadyCompanyIs, CreateView):
    form_class = CompanyForm
    template_name = "vacancies/company_form.html"
    success_url = reverse_lazy("company_update")
    extra_context = {"title": "Создать компанию"}

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f"Компания {form.instance.name} успешно создана!")
        return super().form_valid(form)


class IfNoCompanyYet(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("login")

    def test_func(self):
        return Company.objects.filter(owner=self.request.user).exists()

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return super().handle_no_permission()
        return redirect("lets_start_company")


class UpdateCompany(IfNoCompanyYet, SuccessMessageMixin, UpdateView):
    form_class = CompanyForm
    template_name = "vacancies/company_form.html"
    success_url = reverse_lazy("company_update")
    success_message = "Информация о компании обновлена!"
    extra_context = {"title": "Обновить компанию"}

    def get_object(self, queryset=None):
        return self.request.user.company


class MyVacanciesList(IfNoCompanyYet, ListView):
    template_name = "vacancies/my_vacancies_list.html"

    def get_queryset(self):
        return Vacancy.objects.filter(company=self.request.user.company).annotate(cnt=Count("applications"))


class CreateVacancy(IfNoCompanyYet, CreateView):
    form_class = VacancyForm
    template_name = "vacancies/vacancy_form.html"
    extra_context = {"title": "Создать вакансию"}

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.success(self.request, f"Вакансия *{form.instance.title}* создана!")
        return super().form_valid(form)


class UpdateVacancy(IfNoCompanyYet, UpdateView):
    form_class = VacancyForm
    template_name = "vacancies/vacancy_form.html"
    extra_context = {"title": "Обновить вакансию"}

    def get_object(self, queryset=None):
        return get_object_or_404(Vacancy, company=self.request.user.company, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applications"] = Application.objects.filter(vacancy=self.object)
        context["how_many"] = len(context["applications"])
        return context

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.success(self.request, f"Вакансия *{form.instance.title}* обновлена!")
        return super().form_valid(form)


class IfAlreadyResumeIs(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("login")

    def test_func(self):
        return not Resume.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return super().handle_no_permission()
        return redirect("home_page")


class LetsStartResume(IfAlreadyResumeIs, TemplateView):
    template_name = "vacancies/lets_start_resume.html"


class CreateResume(IfAlreadyResumeIs, CreateView):
    form_class = ResumeForm
    template_name = "vacancies/resume_form.html"
    extra_context = {"title": "Создать резюме"}
    success_url = reverse_lazy("resume_update")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Ваше резюме создано!")
        return super().form_valid(form)


class IfNoResumeYet(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("login")

    def test_func(self):
        return Resume.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        if self.request.user.is_anonymous:
            return super().handle_no_permission()
        return redirect("lets_start_resume")


class UpdateResume(IfNoResumeYet, SuccessMessageMixin, UpdateView):
    form_class = ResumeForm
    template_name = "vacancies/resume_form.html"
    extra_context = {"title": "Обновить резюме"}
    success_url = reverse_lazy("resume_update")
    success_message = "Ваше резюме обновлено!"

    def get_object(self, queryset=None):
        return self.request.user.resume


class Search(ListView):
    template_name = "vacancies/search.html"
    context_object_name = "vacancies"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("s", "")
        return Vacancy.objects.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(specialty__code__icontains=query) |
            Q(specialty__title__icontains=query) |
            Q(company__description__icontains=query)).select_related("company", "specialty")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["s"] = f"s={self.request.GET.get('s', '')}&"
        context["count_vacancies"] = self.object_list.count
        return context


def custom_handler404(request, exception):
    return HttpResponseNotFound("Ресурс не найден!")


def custom_handler500(request):
    return HttpResponseServerError("Ошибка сервера!")
