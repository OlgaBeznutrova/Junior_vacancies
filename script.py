import django
import json
import os

os.environ["DJANGO_SETTINGS_MODULE"] = 'conf.settings'
django.setup()

from vacancies.models import Specialty, Company, Vacancy  # noqa: E402
from vacancies.forms import CompanyForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

if __name__ == "__main__":

# with open("specialties.json", encoding="utf-8") as file:
#       specialties = json.load(file)
#   for specialty_data in specialties:
#       specialty = Specialty.objects.create(
#           code=specialty_data["code"],
#           title=specialty_data["title"],
#       )

#   with open("companies.json", encoding="utf-8") as file:
#       companies = json.load(file)
#   for company_data in companies:
#       company = Company.objects.create(
#           name=company_data["title"],
#           location=company_data["location"],
#           logo=company_data["logo"],
#           description=company_data["description"],
#           employee_count=company_data["employee_count"],
#       )

#   with open("jobs.json", encoding="utf-8") as file:
#       jobs = json.load(file)
#   for jobs_data in jobs:
#       job = Vacancy.objects.create(
#           title=jobs_data["title"],
#           specialty=Specialty.objects.get(code=jobs_data["specialty"]),
#           company=Company.objects.get(id=jobs_data["company"]),
#           skills=jobs_data["skills"],
#           text=jobs_data["description"],
#           salary_min=jobs_data["salary_from"],
#           salary_max=jobs_data["salary_to"],
#           published_at=jobs_data["posted"],
#       )
