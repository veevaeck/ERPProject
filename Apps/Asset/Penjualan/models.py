from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.Property_asset.models import *
from Apps.Hrm.Master_General.models import Department
from Apps.Asset.Master.models import *
from Apps.Asset.Penghapusan.models import *
from Apps.Asset.const import *
from datetime import datetime
from tinymce.models import HTMLField
from PIL import Image
from Apps.Accounting.GeneralLedger.models import Ms_Journal, Ms_Period
from Apps.Accounting.CashBank.models import *
from Apps.Distribution.master_sales.models import PaymentTerm

class Sale(models.Model):
    no_reg = models.CharField(verbose_name='No.Penjualan', max_length=25, editable=False)
    asset = models.OneToOneField(Ms_asset, verbose_name=_('Asset '))
    method_sale = models.IntegerField(verbose_name=_('Metode Penjualan '),choices=metode_penjualan, default=1)

    class Meta:
        verbose_name_plural="Data Penjualan"
        verbose_name="Data Penjualan"

    def incstring(self):
        try:
            data = Sale.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'SALE/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(Sale, self).save()

    def __unicode__(self):
        return '%s' % self.no_reg

class Procurement(models.Model):
    no_reg = models.CharField(verbose_name='No.Procurement', max_length=25, editable=False)
    #header_disposal = models.OneToOneField(Header_disposal_request, verbose_name=_('Header Disposal '))
    sale = models.OneToOneField(Sale, verbose_name=_('No Penjualan'))
    title = models.CharField(verbose_name=_('Judul Penjualan '),max_length=30)
    slug = models.CharField(verbose_name=_('Slug '), max_length=30, blank=True, null=True)
    detail_sale = HTMLField(verbose_name=_('Detail Penjualan '), blank=True, null=True)
    total_price = models.DecimalField(verbose_name=('Harga Awal'), max_digits=20, decimal_places=2, default=0)
    end_enlisting = models.DateTimeField(verbose_name=_('Batas Pendaftaran '))
    sale_add_date = models.DateField(verbose_name=_('Tgl Pembuatan Lelang '), auto_now_add=True)
    end_bid = models.DateTimeField(verbose_name=_('Tgl Batas Penawaran'))
    faktur = models.ForeignKey('Tr_Asset_Sale_Invoice', verbose_name=_('Faktur '))
    #upload_path = 'media/procurement'
    image = models.ImageField(upload_to='uploads', blank=True)
    #image_url = models.URLField(null=True, blank=True)
    published = models.BooleanField(verbose_name=_('Publikasi ? '), default=True)
    payment_method = models.IntegerField(verbose_name=_('Metode Pembayaran '),choices=metode_pembayaran, blank=True, null=True)
    detail_payment = HTMLField(verbose_name=_('Detail Pembayaran '),blank=True, null=True)


    def detail_salex(self):
        return '%s' % self.detail_sale
    detail_salex.allow_tags = True
    detail_salex.short_description = 'Detail Penjualan'

    def winner(self):
        max = 0
        strwinner = '-'
        try:
            data = Customer_proc.objects.filter(procurement__id=self.id)
            for d in data:
                if max < d.bid_value:
                    max = d.bid_value
            win = Customer_proc.objects.filter(procurement__id=self.id, bid_value=max).order_by('-add_date')
            winner = {}
            for w in win:
                winner = Customer_proc.objects.get(id=w.id)
            strwinner = '%(x)s' % {'x':winner.customer.customer_name}
        except:
            pass
        return strwinner

    def display_image(self):
        return '<img src="%s%s" WIDTH="75" HEIGHT="75"/>' % (settings.MEDIA_URL, self.image)

    display_image.short_description = 'Gambar'
    display_image.allow_tags = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if not self.image:
            return

        image  = Image.open(self.image)
        (width, height) = photo.size
        size = (110,110)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image.path)
        super(Procurement, self).save()

    def total(self):
        max = 0
        try:
            data = Customer_proc.objects.filter(procurement__id=self.id)
            for d in data:
                if max < d.bid_value:
                    max = d.bid_value
        except:
            pass
        return max

    def harga_deal(self):
        max = 0
        strharga_akhir = '-'
        try:
            data = Customer_proc.objects.filter(procurement__id=self.id)
            for d in data:
                if max < d.bid_value:
                    max = d.bid_value
            strharga_akhir = '%(x)s' % {'x':max}
        except:
            pass
        return strharga_akhir

    class Meta:
        verbose_name_plural="Procurement"
        verbose_name="Procurement"

    def incstring(self):
        try:
            data = Procurement.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow': strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'PROC/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
        if self.no_reg =='':
            self.no_reg = self.no_rek()
        else:
            self.no_reg = self.no_reg
        super(Procurement, self).save()

    def status(self):
        now = datetime.now().utcnow().date()
        now_t = datetime.now().utcnow().time()
        end_sign = self.end_enlisting.date()
        end_sign_t = self.end_enlisting.time()
        end_bid = self.end_bid.date()
        end_bid_t = self.end_bid.time()
        status = 'Penawaran Ditutup'
        daftar = end_sign-now
        tawar = end_bid-now

        if tawar.days == 0:
            if now_t < end_bid_t:
                status = 'Penawaran Dibuka'
        if tawar.days > 0:
            status = 'Penawaran Dibuka'
        if daftar.days == 0:
            if now_t < end_sign_t:
                status = 'Pendaftaran'
        if daftar.days > 0:
            status = 'Pendaftaran'

        return status

    def harga_awal(self):
        x = self.total_price

        return 'Rp. %(x)s' % {'x':x}

    def __unicode__(self):
        return '%s' % self.no_reg


class Customer_proc(models.Model):
    procurement = models.ForeignKey(Procurement, verbose_name=_('ID Procurement '))
    customer = models.ForeignKey(Ms_customer, verbose_name=_('Customer '))
    bid_value = models.DecimalField(verbose_name=('Nilai Penawaran '), max_digits=20, decimal_places=2, blank=True, null=True)
    add_date = models.DateTimeField(verbose_name=('Tanggal '),auto_now_add=True)

    class Meta:
        verbose_name_plural="Customer Procurement"
        verbose_name="Customer Procurement"

    def nilai_penawaran(self):
        x =(self.bid_value)

        return 'Rp. %(x)s' % {'x':x}

    def ID(self):
        return 'ID: %(id)s | %(name)s' % {'id':self.id,'name':self.customer}
    ID.short_description='ID'


    def __unicode__(self):
        return 'ID: %(id)s | %(name)s' % {'id':self.procurement.no_reg,'name':self.customer}

class Bidding(models.Model):
    custom_proc = models.ForeignKey(Customer_proc, verbose_name=_('Customer Procurement '))
    msg_add_date = models.DateTimeField(verbose_name=_('Tanggal Pengiriman '), auto_now_add=True)
    uname = models.CharField(verbose_name=_('Nama Pengirim '),max_length=50, editable=False, default='admin')
    msg = models.TextField(verbose_name=_('Pesan '))

    class Meta:
        verbose_name_plural="Bidding"
        verbose_name="Biddings"

    def __unicode__(self):
        return '%s' % self.id

class Direct(models.Model):
    #header_disposal = models.OneToOneField(Header_disposal_request, verbose_name=_('Header Disposal '),blank=True , null=True)
    sale = models.OneToOneField(Sale, verbose_name=_('No Penjualan'))
    customer_name = models.ForeignKey(Ms_customer, verbose_name=('Nama Pembeli'), max_length=50)
    detail_sale = HTMLField(verbose_name=_('Detail Penjualan '), blank=True, null=True)
    total_price = models.DecimalField(verbose_name=('Harga Total'), max_digits=20, decimal_places=2)
    sale_add_date = models.DateField(verbose_name=_('Tgl Pejualan '), auto_now_add=True)
    payment_method = models.IntegerField(verbose_name=_('Metode Pembayaran '),choices=metode_pembayaran, default=1)
    detail_payment = models.TextField(verbose_name=_('Detail Pembayaran '),blank=True, null=True)
    faktur = models.ForeignKey('Tr_Asset_Sale_Invoice', verbose_name=_('Faktur '))

    def harga_total(self):
        x = self.total_price

        return 'Rp. %(x)s' % {'x':x}

    class Meta:
        verbose_name_plural="Direct"
        verbose_name="Direct"

    def detail_salex(self):
        return '%s' % self.detail_sale
    detail_salex.allow_tags = True
    detail_salex.short_description = 'Detail Penjualan'

    def detail_paymentx(self):
        return '%s' % self.detail_payment
    detail_paymentx.allow_tags = True
    detail_paymentx.short_description = 'Detail Pembayaran'

    def __unicode__(self):
        return '%s' % self.id

class Tr_Asset_Sale_Invoice(models.Model):
    no_reg = models.CharField(verbose_name='No.Invoice ', max_length=25, editable=False)
    customer = models.ForeignKey(Ms_customer, verbose_name='Nama Pembeli ')
    date = models.DateField(verbose_name='Tanggal Pembelian')
    period = models.ForeignKey(Ms_Period, related_name=_('Periode '))
    journal = models.ForeignKey(Ms_Journal, related_name=_('Tipe Jurnal '))
    payment_term = models.ForeignKey(PaymentTerm, verbose_name=_('Jangka Waktu '))
    currency = models.ForeignKey(Ms_Currency, related_name=_('Mata Uang '))
    tax = models.ForeignKey(Ms_Tax, related_name=_('Pajak '))
    info = models.TextField(verbose_name='Info Tambahan ')
    total = models.DecimalField(verbose_name=('Total '), max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name_plural="Faktur Penjualan"
        verbose_name="Faktur Penjualan"

    def incstring(self):
        try:
            data = Tr_Asset_Sale_Invoice.objects.all()
            jml = data.count()
        except:
            jml=0
        pass
        no = 0
        if jml == 0:
            no = 0
        else:
            for d in data:
                split = str(d.no_reg).split('/')
                no = int(split[3])
        num = no + 1
        cstring = str(num)
        return cstring

    def inclen(self):
        leng = len(self.incstring())
        return leng

    def no_rek(self):
        date = datetime.now()
        now = date.strftime("%m")
        nowyear = date.strftime("%Y")
        intnow = int(now)
        intyear = int(nowyear)
        strnow = str(intnow)
        if len(strnow) < 2 :
            strnow = '0%(strnow)s' % {'strnow' : strnow}
        nol = 5 - self.inclen()
        if nol == 1: num = "0"
        elif nol == 2: num = "00"
        elif nol == 3: num = "000"
        elif nol == 4: num = "0000"
        number = num + self.incstring()
        return 'INVOICE/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}

    def total(self):
        total = 1
        try:
            direct = Direct.objects.filter(faktur__id=self.id)
            for d in direct:
                total += d.total_price
        except:
            pass

        try:
            proc = Procurement.objects.filter(faktur__id=self.id)
            for d in direct:
                total += d.total()
        except:
            pass
        return total
    total.short_description = 'Harga Total'

    def period(self):
        today = datetime.now().date()
        a = 0
        try:
            per = Ms_Period.objects.filter(Start_Period__lte=today, End_Period__gte=today)
            a = per.count()
        except:
            pass
        if a == 1:
            for x in per:
                b = x.Code
                c = Ms_Period.objects.get(Code=b)
        else:
            c = self.Period
        return c

    def journal(self):
        a = Ms_Journal.objects.get(Type=1)
        return a

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.no_reg == '':
            self.no_reg = self.no_rek()
        else: self.no_reg = self.no_reg
        self.period = self.period()
        self.journal = self.journal()
        self.total = self.total()
        models.Model.save(self, force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return '%s' % self.no_reg
