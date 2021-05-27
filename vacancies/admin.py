from django.contrib import admin

from .models import Company, Vacancy, Specialty, Application


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'employee_count', 'owner')
    list_display_links = ('id', 'name')


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'specialty', 'company', 'salary_min', 'salary_max', 'published_at')
    list_display_links = ('id', 'title')


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title')
    list_display_links = ('id', 'code')


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Application, ApplicationAdmin)
