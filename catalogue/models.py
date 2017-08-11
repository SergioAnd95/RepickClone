from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.urls import reverse

from taggit.managers import TaggableManager


from urllib.parse import urlparse
# Create your models here.


class Category(models.Model):
    """
    Represent Category
    """
    class CategoryType:
        CATEGORY = 1
        GIFT = 2

        CATEGORY_TYPE_CHOICES = (
            (CATEGORY, _('Катеогрия')),
            (GIFT, _('Подарок'))
        )

    name = models.CharField(
        _('Название'),
        max_length=30,
        unique=True
    )
    main_image = models.ImageField(_('Изображение'), upload_to='categories')
    type = models.IntegerField(
        _('Тип'),
        choices=CategoryType.CATEGORY_TYPE_CHOICES
    )
    slug = models.SlugField(_('Ссылка'), unique=True)

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name

    #@permalink
    def get_absolute_url(self):
        return reverse('catalogue:category_detail', None, (self.slug, ))


class Brand(models.Model):
    """
    Represent brand
    """
    name = models.CharField(_('Название'), max_length=30)
    main_image = models.ImageField(_('Изображение'), upload_to='brands')
    slug = models.SlugField(_('Ссылка'), unique=True)

    class Meta:
        verbose_name = _('Брэнд')
        verbose_name_plural = _('Брэнды')

    def __str__(self):
        return self.name


class Item(models.Model):
    """
    Represent Item
    """
    main_image = models.ImageField(_('Изображение'), upload_to='items')
    title = models.CharField(_('Название'), max_length=120)
    price = models.DecimalField(_('Цена'), max_digits=10, decimal_places=2)
    link = models.URLField(_('Ссылка на внешний рессурс'))
    description = models.TextField(_('Описание'))
    site_name = models.CharField(
        _('Название сайта'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('из поля "Ссылка" имя сайта береться автоматически, '
                    'не стоит заполнять это поля если имя сайта вас устраивает')
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name=_('Категории'),
        related_name='items'
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name=_('Производитель'),
        related_name='items'
    )
    when_created = models.DateTimeField(_('Когда создан'), auto_now_add=True)
    slug = models.SlugField(_('Ссылка на товар'), unique=True)

    tags = TaggableManager()
    enable = models.BooleanField(_('Есть в наличии'), default=True)

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
        ordering = ('-when_created', )

    def __str__(self):
        return self.title

    @property
    def get_site_name(self):
        if not self.site_name:
            domain = urlparse(self.link).netloc.replace('www.', '')
            domain = domain[0:domain.rfind('.')].capitalize()
            return domain

        return self.site_name

    @property
    def get_parse_price(self):
        d = str(self.price)
        parse = d.split('.')
        return {'digits': parse[0], 'decimal': parse[1]}