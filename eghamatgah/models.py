from django.db import models
from seller_account.models import Seller
from user_account.models import User
from django.core.validators import FileExtensionValidator





class Eghamatgah_Category(models.Model):
    parent = models.ForeignKey('Eghamatgah_Category', null=True,
                               related_name='parenteghamatcategory', on_delete=models.CASCADE,
                               blank=True, verbose_name='دسته بندی والد')
    title = models.CharField(max_length=300, verbose_name='عنوان دسته بندی')
    url_title = models.CharField(max_length=200, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی اقامتگاه'
        verbose_name_plural = 'دسته بندی های اقامتگاه ها'


class Eghamatgah(models.Model):
    type = (
        ('villa', 'ویلا'),
        ('aparteman', 'آپارتمان'),
        ('khanebagh', 'خانه باغ'),
        ('kolbe', 'کلبه'),
    )
    Ecategory = models.ManyToManyField(Eghamatgah_Category, blank=True, related_name='categories', verbose_name='دسته بندی')
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE, related_name='seller', verbose_name='فروشنده')
    title = models.CharField(max_length=100, verbose_name='عنوان اقامتگاه')
    eghamat_type= models.CharField(max_length=100, choices=type, verbose_name='نوع اقامتگاه')
    ostan = models.CharField(max_length=20, verbose_name='استان')
    shahr = models.CharField(max_length=20, verbose_name='شهر')
    address = models.CharField(max_length=300, verbose_name='آدرس کامل')
    tedad_otagh = models.PositiveIntegerField(null=True, verbose_name='تعداد اتاق')
    metrazh = models.PositiveIntegerField(null=True, verbose_name='متراژ')
    zarfiat = models.PositiveIntegerField(null=True, verbose_name='ظرفیت')
    zarfiat_extra = models.DecimalField(max_digits=10,decimal_places=2, default=0, verbose_name='تعداد نفرات اضافه')
    gheymat_har_shab = models.IntegerField(null=True, verbose_name='قیمت هر شب')
    time_voroud = models.TimeField(null=True, verbose_name='تایم ورود')
    time_khorouj = models.TimeField(null=True, verbose_name='تایم خروج')
    description = models.CharField(max_length=200, verbose_name='توضیحات تکمیلی')
    wifi = models.BooleanField(default=False, verbose_name='اینترنت وای فای')
    parking = models.BooleanField(default=False, verbose_name='پارکینگ')
    pool = models.BooleanField(default=False, verbose_name='استخر')
    kitchen = models.BooleanField(default=False, verbose_name='آشپزخانه')
    tv = models.BooleanField(default=False, verbose_name='تلویزیون')
    image = models.ImageField(upload_to='media',default='', verbose_name='تصویر1')
    image2 = models.ImageField(upload_to='media',default='', verbose_name='تصویر2')
    image3 = models.ImageField(upload_to='media',default='', verbose_name='تصویر3')
    image4 = models.ImageField(upload_to='media',default='', verbose_name='تصویر4')
    image5 = models.ImageField(upload_to='media',default='', verbose_name='تصویر5')
    video = models.FileField(
        upload_to='videos',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi'])],
        verbose_name='ویدیو'
    )
    aparat_video_id = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مشخصات اقامتگاه'
        verbose_name_plural = 'مشخصات اقامتگاه ها'




class UnavailableDate(models.Model):
    eghamat = models.ForeignKey(Eghamatgah, on_delete=models.CASCADE, related_name='unavailable_dates')
    date = models.DateField()

    def __str__(self):
        return f"{self.eghamat.title} - {self.date}"


class AvailableDate(models.Model):
    eghamat = models.ForeignKey(Eghamatgah, on_delete=models.CASCADE, related_name='available_dates')
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(verbose_name='تاریخ پایان')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت روز')

    def __str__(self):
        return f"{self.eghamat.title} | {self.start_date} تا {self.end_date} | {self.price} تومان"

    class Meta:
        verbose_name = 'بازه تاریخ قابل رزرو'
        verbose_name_plural = 'بازه های تاریخ‌های قابل رزرو'

class EghamatComment(models.Model):
    STAR_TYPE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),

    )
    eghamat = models.ForeignKey(Eghamatgah, on_delete=models.CASCADE, verbose_name='اقامتگاه')
    parent = models.ForeignKey('EghamatComment', null=True,blank=True,on_delete=models.CASCADE,related_name='parentcomment', verbose_name='والد')
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن نظر')
    star = models.CharField(max_length=20, choices=STAR_TYPE, verbose_name='امتیاز')
    booking = models.OneToOneField('booking.Booking',on_delete=models.CASCADE,default='',null=True,blank=True, verbose_name='رزرو مربوطه')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'نظر اقامتگاه'
        verbose_name_plural = 'نظرات اقامتگاه'

