from importlib import resources
from django.contrib import admin
from .models import Transaction, Goal
from import_export.admin import ExportMixin
from .models import Goal
from import_export import resources
    

class TransactionAdmin(resources.ModelResource):
    class Meta:
        model = Transaction 
        fields=('date','title','amount','Transaction_type')


class TransctionAdminView(ExportMixin, admin.ModelAdmin):
    resource_class = TransactionAdmin
    list_display = ('user','date','title','amount','Transaction_type')
    list_filter = ('Transaction_type','date')
    search_fields = ('title','amount')        

# Register your models here. 
from .models import Transaction
admin.site.register(Transaction, TransctionAdminView)  
admin.site.register(Goal)