import os
import django
import json

os.environ["DJANGO_SETTINGS_MODULE"] = 'conf.settings'
django.setup()

from django.shortcuts import get_list_or_404
from vacancies.models import Specialty, Company, Vacancy
from django.db.models import Count

if __name__ == "__main__":
    #bbb = Vacancy.objects.values("id", "title", "specialty__title")
    #for b in bbb:
        #print(b["id"], b["title"], b["specialty__title"])
    #vacancies = Vacancy.objects.select_related("specialty", "company")
    #print(vacancies.count())
    #for vacancy in vacancies:
    #    print(vacancy.title, vacancy.specialty.title, vacancy.skills, vacancy.company.name, vacancy.company.location,
    #          vacancy.published_at, vacancy.salary_min, vacancy.salary_max, vacancy.company.logo)
    title = Specialty.objects.get(code="backend").title
    print(title)
    vacancies = Vacancy.objects.filter(specialty__title="Бэкенд")
    for vacancy in vacancies:
        print(vacancy.title, vacancy.specialty.title, vacancy.company.logo)
    print(vacancies)






#    with open("specialties.json", encoding="utf-8") as file:
#        specialties = json.load(file)
#    for specialty_data in specialties:
#        specialty = Specialty.objects.create(
#            code=specialty_data["code"],
#            title=specialty_data["title"],
#        )
#
#    with open("companies.json", encoding="utf-8") as file:
#        companies = json.load(file)
#    for company_data in companies:
#        company = Company.objects.create(
#            name=company_data["title"],
#            location=company_data["location"],
#            logo=company_data["logo"],
#            description=company_data["description"],
#            employee_count=company_data["employee_count"],
#        )
#
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
