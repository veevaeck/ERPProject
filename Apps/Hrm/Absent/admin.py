''' @author: Fery Febriyan Syah '''


from django.contrib import admin
from Apps.Hrm.Absent.models import *

class Header_AbsentAdmin (admin.ModelAdmin):
    list_display = ('date_now','day_status','period', 'lock',)
    
    def suit_row_attributes(self, obj, request):
        css_class = {
            True:'success', False: 'error',}.get(obj.lock)
        if css_class:
            return {'class': css_class, 'data': obj.lock}
    
    def get_readonly_fields(self, request, object=None):
        readonly_fields = ()
        if getattr(object, 'lock', None) == True:
            readonly_fields += ('date_now',)
          
        return readonly_fields
    
admin.site.register(Header_Absent, Header_AbsentAdmin)

class Data_AbsentAdmin (admin.ModelAdmin):
    list_display = ('header','employee','start_work','end_work','lembur','Total_Rupiah',)
    search_field = ['employee']
    
    def get_form(self, request, object=None, **kwargs):
        form = super(Data_AbsentAdmin, self).get_form(request, object, **kwargs)
        xx = False
        try:
            x = getattr(object, 'header', None)
            xx = x.lock
        except: pass
        
        if xx == False:
            form.base_fields['header'].queryset = form.base_fields['header'].queryset.filter(lock=False)
        else:
            readonly_fields = ('header','employee','start_work','end_work')
        return form 
    
admin.site.register(Data_Absent, Data_AbsentAdmin)

