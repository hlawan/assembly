from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Member)
admin.site.register(models.MonthlyContribution)
admin.site.register(models.Donation)
