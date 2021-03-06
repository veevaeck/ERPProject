from django.contrib import admin
from Apps.Distribution.invoice.models import ReceivableInvoice, DetailFaktur
from Apps.Distribution.order.models import SalesOrder
from django import forms
from suit.widgets import AutosizedTextarea, SuitDateWidget, EnclosedInput, Select
from Apps.Distribution.customer.models import Company
from django_select2 import AutoModelSelect2Field, AutoHeavySelect2Widget
from library.const.order import INVOICE_FINISH_STATUS
from django.utils.translation import ugettext_lazy as _

class CorpChoices(AutoModelSelect2Field):
    queryset = Company.objects.all()
    search_fields = ['corporate__icontains']

class SOChoices(AutoModelSelect2Field):
    queryset = SalesOrder.objects.filter(status=3)
    search_fields = ['number__icontains']


class FormInvoiceOrder(forms.ModelForm):
    corp_verbose_name = 'Nama Perusahaan'
    customer = CorpChoices(label=corp_verbose_name.capitalize(),
                           widget=AutoHeavySelect2Widget(select2_options=
                                                              {'width': '220px', 'placeholder': 'Cari %s ...'
                                                                                                % corp_verbose_name}))
    so_verbose_name = 'Nomer SO'
    so_reff = SOChoices(label=so_verbose_name.capitalize(),
                           widget=AutoHeavySelect2Widget(select2_options=
                                                              {'width': '220px', 'placeholder': 'Cari %s ...'
                                                                                                % so_verbose_name}))
    class Meta:
        model = ReceivableInvoice
        widgets = {
            'quotation': AutosizedTextarea(attrs={'rows': '3'}),
            'term_service': AutosizedTextarea(attrs={'rows': '3'}),
            'shipping_address': AutosizedTextarea(attrs={'rows': '3'}),
            'date': SuitDateWidget
        }


class FormItemInline(forms.ModelForm):
    class Meta:
        widgets = {
            'capacity': EnclosedInput(append='ml', attrs={'class': 'input-small'}),
            'height': EnclosedInput(append='mm', attrs={'class': 'input-small'}),
            'quantity': EnclosedInput(attrs={'class': 'input-small'}),
            'price': EnclosedInput(attrs={'class': 'input-large'}),
            'weight': EnclosedInput(append='gr', attrs={'class': 'input-small'}),
            'diameter': EnclosedInput(append='mm', attrs={'class': 'input-small'}),
            'color': Select(attrs={'class': 'input-medium'}),
        }

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

class ProductImage(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name=str(value)
            output.append(u' <a href="%s" target="_blank"><img width="100px" height="110px" src="%s" alt="%s" /></a> %s ' % \
                (image_url, image_url, file_name, _(' ')))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class ItemInline(admin.StackedInline):
    form = FormItemInline
    model = DetailFaktur
    extra = 1
    verbose_name_plural = 'Detail Order Item'
    can_delete = True
    fieldsets = [
        (None, {
            'fields': ['color', 'category', ('weight', 'capacity'), ('height', 'diameter'), 'image', 'label', 'quantity'
            , 'price']
        })
    ]

    def get_formset(self, request, obj=None):
        formset = super(ItemInline, self).get_formset(request, obj)

        if obj is not None and obj.status in (INVOICE_FINISH_STATUS):
            formset.max_num = 0
            formset.can_delete = False
        if obj is not None:
            formset.extra = 0
        return formset

    def get_readonly_fields(self, request, obj=None):
        readonly = super(ItemInline, self).get_readonly_fields(request, obj)

        if getattr(obj, 'status', None) in (INVOICE_FINISH_STATUS):
            readonly = ('color', 'category', 'capacity', 'height', 'weight', 'diameter', 'image', 'label', 'quantity', 'price')
        return readonly

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'image':
            request = kwargs.pop("request", None)
            kwargs['widget'] = ProductImage
            return db_field.formfield(**kwargs)
        elif db_field.name == 'label':
            request = kwargs.pop("request", None)
            kwargs['widget'] = ProductImage
            return db_field.formfield(**kwargs)
        return super(ItemInline,self).formfield_for_dbfield(db_field, **kwargs)


class InvoiceAdmin(admin.ModelAdmin):
    form = FormInvoiceOrder
    list_display = ['number', 'tax', 'payment_term', 'payment_type', 'shipping_methods', 'sales_person']
    list_filter = ['payment_term', 'payment_type', 'shipping_methods', 'status']
    search_fields = ['number', 'customer']
    inlines = [ItemInline]
    #def save_model(self, request, obj, form, change):
    #    from Apps.Distribution.master_sales.models import StaffPerson
    #    from django.core.exceptions import ObjectDoesNotExist
    #    try:
    #        staff = StaffPerson.objects.get(user=request.user)
    #        if staff:
    #            obj.sales_person = staff
    #            obj.save()
    #    except: ObjectDoesNotExist
admin.site.register(ReceivableInvoice, InvoiceAdmin)
