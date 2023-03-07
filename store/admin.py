from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Customer)
admin.site.register(models.Dealer)
admin.site.register(models.Employee)
admin.site.register(models.Medicine)
admin.site.register(models.Cart)
admin.site.register(models.HistoryPaid)

