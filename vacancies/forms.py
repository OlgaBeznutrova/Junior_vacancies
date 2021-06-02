from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms

from .models import Company, Vacancy, Application, Resume


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


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ("id", "created_at", "updated_at", "user")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["salary"].label = "Ожидаемое вознаграждение"
        self.fields["portfolio"].label = "Ссылка на портфолио"
        self.fields['education'].widget = forms.Textarea(attrs={'rows': 3})
        self.helper.layout = Layout(
            Row(
                Column("name"),
                Column("surname"),
            ),
            Row(
                Column("status"),
                Column("salary"),
            ),
            Row(
                Column("specialty"),
                Column("grade"),
            ),
            "education",
            "experience",
            "portfolio",
            Submit("submit", "Сохранить", css_class='btn-info'),
        )
