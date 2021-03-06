__author__ = 'FARID ILHAM Al-Q'
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
from library.const.country import COUNTRIES

REFERRAL = (
    ('1', _('Friend')), ('2', _('Search Engine')), ('3', _('Newspaper')), ('4', _('Magazine')), ('5', _('Others'))
)


class Contacts(models.Model):
    name = models.CharField(verbose_name=_('Nama Lengkap '), max_length=50)
    email = models.EmailField(verbose_name=_('E-mail  '))
    phone = models.CharField(verbose_name=_('Telepon '), max_length=15)
    company = models.CharField(verbose_name=_('Perusahaan '), max_length=50,
                               help_text=_('*) Isi dengan nama perusahaan'))
    country = models.CharField(verbose_name=_('Negara '), max_length=50, choices=[(x[0], x[3]) for x in COUNTRIES])
    referral = models.CharField(verbose_name=_('Tahu website ini dari '), max_length=50, choices=REFERRAL)
    comment = RichTextField(verbose_name=_('Komentar '))
    pub_date = models.DateTimeField(verbose_name=_('Publikasi '), auto_now=False, auto_now_add=True)

    def __str__(self):
        return '%s : %s' % (self.company, self.name)

    class Meta:
        verbose_name = _('Buku Tamu')
        ordering = ['-pub_date']
        verbose_name_plural = _("Buku Tamu")
        db_table = "Distribusi | Buku Tamu"


class News(models.Model):
    title = models.CharField(verbose_name=_('Judul'), max_length=50)
    slug = models.SlugField(unique=True)
    content = RichTextField(verbose_name=_('Berita'))
    pub_date = models.DateTimeField(verbose_name=_('Publikasi'), auto_now=False, auto_now_add=True)
    update = models.DateTimeField(verbose_name=_('Update'), auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = _('Berita Terkini')
        verbose_name = _('Berita Terkini')
        db_table = "Distribusi | Berita Terkini"


COMPLAINT_STATUS = [('1', _('Draft')), ('2', _('On Progress')), ('3', _('Finished'))]
ABOUT_COMPLAINT = [('1', _('Pesanan')), ('2', _('Pengiriman')), ('3', _('Pembayaran')), ('4', _('Retur')), ('5', _('Others'))]

from Apps.Distribution.customer.models import Company


class Complaint(models.Model):
    customer = models.ForeignKey(Company, verbose_name=_("Nama Perusahaan "))
    title = models.CharField(verbose_name=_("Judul Komplain "), max_length=50)
    about = models.CharField(verbose_name=_("Jenis Komplain "), max_length=50, choices=ABOUT_COMPLAINT)
    status = models.CharField(verbose_name=_("Status "), choices=COMPLAINT_STATUS, default=1, max_length=50)
    description = models.TextField(verbose_name=_("Keluhan/Komplain "))
    created = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_("Tanggal Komplain "))

    class Meta:
        ordering = ['-created']
        verbose_name_plural = _("Komplain / Keluhan")
        verbose_name = _("Komplain / Keluhan")
        db_table = "Distribusi | Komplain / Keluhan"
