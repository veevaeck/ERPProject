""" @author: Rhiyananta Catur Yudowicitro """

from django.contrib import admin
from Apps.Inventory.Property_Inv.models import *
from django.utils.translation import ugettext_lazy as _

class Jenis_satuanAdmin (admin.ModelAdmin):
    list_display = ('type_satuan',)
    search_field = ['type_satuan']
    
admin.site.register(Jenis_satuan, Jenis_satuanAdmin)

class type_commodityAdmin (admin.ModelAdmin):
    list_display = ('type_commodity',)
    search_field = ['type_commodity']
    
admin.site.register(type_commodity, type_commodityAdmin)

class quantity_commodityAdmin (admin.ModelAdmin):
    list_display = ('quantity_commodity',)
    search_field = ['quantity_commodity']
    
admin.site.register(quantity_commodity, quantity_commodityAdmin)

class Role_user_admin(admin.ModelAdmin):
    list_display = ['user','access_level','intern_date_register']
        
admin.site.register(Role_user, Role_user_admin)


class DepartmentAdmin (admin.ModelAdmin):
    list_display = ('department',)
    search_field = ['department']
    
admin.site.register (Department, DepartmentAdmin)
