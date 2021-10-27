from django.contrib import admin

from .models import Company

admin.site.register(Company)

# @admin.register(Company)
# class CompanyAdmin(admin.ModelAdmin):
#     pass
