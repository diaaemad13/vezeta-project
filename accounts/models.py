from distutils.command.upload import upload
from email.headerregistry import Address
# from datetime import datetime
from django.db import models
from django.db.models import OneToOneField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.utils.text import slugify

# Create your models here.

TYPE_OF_PERSON=(
    ('M' , "Male"),
    ('F' , "Female"),
)

class Profile(models.Model):
    user = OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    name = models.CharField(_("الأسم:"), max_length=30, blank=True, null=True)
    subtitle = models.CharField(_("نبذة عنك:"), max_length=100, blank=True, null=True)
    address = models.CharField(_("المحافظه:"), max_length=50, blank=True, null=True)
    numberphone = models.CharField(_("رقم الهاتف:"), max_length=14, blank=True, null=True)
    workhour = models.CharField(_("عدد ساعات العمل :"), max_length=4, blank=True, null=True)
    waittime = models.IntegerField(_("مدة الانتظار"), blank=True, null=True)
    who_i = models.TextField(_("من انا:"), max_length=250, blank=True, null=True)
    price = models.IntegerField(_("السعر:"), blank=True, null=True)
    image = models.ImageField(_("الصورة الشخصية"), upload_to='Profile', blank=True, null=True)
    spicialist = models.CharField(_("متخصص في :"), max_length=50, blank=True, null=True)
    type_of_person = models.CharField(_("النوع"), choices= TYPE_OF_PERSON, max_length=50, blank=True, null=True)
    twiter = models.CharField(_("تويتر"), max_length=100, blank=True, null=True)
    facebook = models.CharField(_("فيسبوك"), max_length=100, blank=True, null=True)
    gmail = models.CharField(_("جميل"), max_length=100, blank=True, null=True)
    slug = models.SlugField(_("slug"), blank=True, null=True)


    def save (self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)




    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


    def __str__(self):
        return '%s' %(self.user.username)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user = kwargs['instance'])

post_save.connect(create_profile, sender = User)



