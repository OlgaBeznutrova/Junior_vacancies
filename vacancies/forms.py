from django import forms

from .models import Company, Vacancy, Application


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("name", "logo", "location", "description", "employee_count")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
        }


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ("title", "specialty", "skills", "text", "salary_min", "salary_max")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "specialty": forms.Select(attrs={"class": "form-control"}),
            "skills": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 7}),
            "salary_min": forms.NumberInput(attrs={"class": "form-control"}),
            "salary_max": forms.NumberInput(attrs={"class": "form-control"}),
            "views": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Вакансия на должность",
            "specialty": "Специальность",
            "company": "Компания",
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("written_username", "written_phone", "written_cover_letter")
        widgets = {
            "written_username": forms.TextInput(attrs={"class": "form-control"}),
            "written_phone": forms.TextInput(attrs={"class": "form-control"}),
            "written_cover_letter": forms.Textarea(attrs={"class": "form-control", "rows": 7}),
        }
        labels = {
            "written_username": "Вас зовут",
            "written_phone": "Ваш телефон",
            "written_cover_letter": "Сопроводительное письмо",
        }
        error_messages = {
            "written_phone": {"invalid": "Неверный формат номера, используйте +X XXX XXX XX XX"},
        }
