from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportMixin
from .models import Eat, Hour


# Register your models here.
class MyImportMixIn(ImportMixin):
    from_encoding = 'utf-8'
    
class DataAdmin(ImportExportModelAdmin, MyImportMixIn):
    pass

admin.site.register(Eat, DataAdmin)
admin.site.register(Hour, DataAdmin)