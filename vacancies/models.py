from django.db import models


class Specialty(models.Model):
    code = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    picture = models.URLField(default="https://place-hold.it/100x60")

    def __str__(self):
        return self.code


class Company(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    logo = models.URLField(default="https://place-hold.it/100x60")
    description = models.TextField(max_length=1000)
    employee_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}{self.location}"


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.PROTECT, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.CharField(max_length=250)
    text = models.TextField(max_length=1000)
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    published_at = models.DateField()

    def __str__(self):
        return self.title
