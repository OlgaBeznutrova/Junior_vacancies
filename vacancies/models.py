from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=30, verbose_name="Код")
    title = models.CharField(max_length=100, verbose_name="Название")
    picture = models.ImageField(upload_to="specialty_logo", default="https://place-hold.it/100x60",
                                verbose_name="Логотип")

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("vacancies_by_category", kwargs={"category_code": self.code})

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название компании")
    location = models.CharField(max_length=50, verbose_name="Город")
    logo = models.ImageField(upload_to="company_logo", default="https://place-hold.it/100x60", verbose_name="Логотип")
    description = models.TextField(max_length=1000, verbose_name="Информация о компании")
    employee_count = models.PositiveIntegerField(verbose_name="Кол-во сотрудников")
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Владелец")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"


class Vacancy(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.CharField(max_length=250, verbose_name="Требования")
    text = models.TextField(max_length=1000, verbose_name="Описание")
    salary_min = models.PositiveIntegerField(verbose_name="Зарплата от...")
    salary_max = models.PositiveIntegerField(verbose_name="Зарплата до...")
    published_at = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    views = models.IntegerField(default=0, verbose_name="Кол-во просмотров")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vacancy_update', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ["-published_at"]


class Application(models.Model):
    written_username = models.CharField(max_length=50)
    written_phone = PhoneNumberField(region="RU")
    written_cover_letter = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")

    def __str__(self):
        return f"{self.written_username}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
