from django.db import models
from django.utils.translation import ugettext as _
from Apps.Asset.Property_asset.models import *
from Apps.Hrm.Master_General.models import Department
from Apps.Asset.Master.models import *
from Apps.Asset.Request.models import *
from datetime import datetime
from tinymce.models import HTMLField

class Header_request_asset(models.Model):
	no_reg = models.CharField(verbose_name='No. Reg Pengadaan', max_length=25, editable=False)
	department = models.ForeignKey(Department, verbose_name=_('Nama Department '))
	ra_add_date = models.DateField(verbose_name=_('Tanggal '),auto_now_add=True)
	ra_lock = models.BooleanField(verbose_name=_('Persetujuan ?'), default=False)
	ra_lock_date = models.DateField(verbose_name=_('Batas Persetujuan '))
	asset_staff_review = models.TextField(verbose_name=_('Asset Staff Review '), blank=True, help_text='Masukkan Kriteria Pengadaan disini.')
	
	class Meta:
		verbose_name_plural="Header Request Asset"
		verbose_name="Header_request_asset"
	
	def incstring(self):
		try:
			data = Header_request_asset.objects.all()
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
		return 'PA/%(year)s/%(month)s/%(unik)s' % {'year': intyear, 'month': strnow, 'unik': number}
	
	def save(self, force_insert=True, force_update=True, using=None, update_fields=None):
		if self.no_reg =='':
			self.no_reg = self.no_rek()
		else:
			self.no_reg = self.no_reg
		super(Header_request_asset, self).save()
		
	def __unicode__(self):
		return u'%s' % self.no_reg

class Data_request_asset(models.Model):
	header_request = models.ForeignKey(Header_request_asset, verbose_name=_('Header Request Asset  '))
#	no_item = models.IntegerField(verbose_name=_('No.Item  '))
	request = models.OneToOneField(Data_user_request, related_name=_('Data Request '), blank=True, null=True, help_text='Pilih Request Pengadaan dari Permintaan Pengadaan')
	#request_change = models.OneToOneField(Data_user_request, related_name=_('Data Request '), blank=True, null=True ,help_text='Pilih Request Pengadaan dari Permintaan Pengadaan')
	unit_of_measure = models.ForeignKey(Unit_of_measure_asset, verbose_name=_('Satuan '), blank=True, null=True)
	ra_used = models.DateField(verbose_name=_('Waktu Penggunaan '), blank=True, null=True)
	ra_amount = models.IntegerField(verbose_name=_('Jumlah '), blank=True, null=True)
	description = HTMLField(verbose_name=_('Deskripsi'), blank=True, help_text='Deskripsi Pengadaan ')
#	currency = models.ForeignKey(Asset_currency, verbose_name=_('Mata Uang '))
#	ra_unit_price = models.DecimalField(verbose_name=_('Harga Per Unit '),decimal_places=2, max_digits=10)
#	asset = models.ForeignKey(Ms_asset, verbose_name=_('Nama Asset'))
	

	class Meta:
		verbose_name_plural="Data Request Asset"
		verbose_name="Data_request_asset"
	
#	def desc(self):
#		des = Data_user_request.objects.get(id=self.request.id)
#		return des.description
#	desc.short_description='Deskripsi'	
	
	def descriptionx(self):
		return '%s' % self.description
	descriptionx.allow_tags = True
	descriptionx.short_description = 'Asset Staff Review'	
	
	def __unicode__(self):
		return  u'%s' % self.header_request
