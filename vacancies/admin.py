from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Company, Vacancy, Specialty, Application, Resume


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location", "employee_count", "owner", "get_logo")
    list_display_links = ("id", "name")
    list_filter = ("location",)

    def get_logo(self, obj):
        if obj.logo:
            return mark_safe(f"<img src='{obj.logo.url}' width=75>")
        return "-"

    get_logo.short_description = "Логотип"


class VacancyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "specialty", "company", "published_at", "views")
    list_display_links = ("id", "title")
    list_filter = ("published_at",)
    fields = ("title", "specialty", "company", "skills", "text", "salary_min", "salary_max", "published_at", "views")
    readonly_fields = ("published_at", "views")


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "title")
    list_display_links = ("id", "code")


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "written_username", "written_phone", "vacancy", "user")
    list_display_links = ("id", "written_username")


class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "surname", "status", "specialty", "grade", "created_at", "updated_at")
    list_display_links = ("id", "name")
    list_filter = ("specialty", "grade", "status", "created_at", "updated_at")
    fields = (
        "user", "name", "surname", "status", "specialty", "grade", "education", "experience", "salary", "portfolio",
        "updated_at", "created_at",
    )
    readonly_fields = ("user", "updated_at", "created_at")


admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Resume, ResumeAdmin)
