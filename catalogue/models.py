from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink, F, Count

import os

from taggit.managers import TaggableManager
from taggit.models import Tag

from urllib.parse import urlparse
# Create your models here.


class ItemManager(models.Manager):
    """ORM item manager"""
    def get_queryset(self):
        return super(ItemManager, self).get_queryset().annotate(total_likes=F('additional_likes')+Count('likes'))


class Category(models.Model):
    """
    Represent Category
    """
    def get_upload_path(self, filename):
        if self.type == self.CategoryType.GIFT:
            name = 'gift'
        else:
            name = 'category'

        return os.path.join(
            name, "%s_%s" % (name, self.slug), filename)

    class CategoryType:
        CATEGORY = 1
        GIFT = 2

        CATEGORY_TYPE_CHOICES = (
            (CATEGORY, _('Category')),
            (GIFT, _('Gift'))
        )

    logo_image = models.ImageField(
        _('Logo image'),
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    background_image = models.ImageField(
        _('Background image'),
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    description = models.TextField(_('Description'))
    name = models.CharField(
        _('Name'),
        max_length=30,
        unique=True
    )
    main_image = models.ImageField(_('Main image'), upload_to=get_upload_path)
    type = models.IntegerField(
        _('Тип'),
        choices=CategoryType.CATEGORY_TYPE_CHOICES
    )
    slug = models.SlugField(_('Slug'), unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        if self.type == 1:
            return 'catalogue:category_detail', (self.slug, )
        elif self.type == 2:
            return 'catalogue:gift_detail', (self.slug, )

    @property
    def get_tags(self):
        tags = Tag.objects.filter(item__categories__in=[self]).distinct()
        return tags


class Brand(models.Model):
    """
    Represent brand
    """
    def get_upload_path(self, filename):

        return os.path.join(
            'brand', "%s_%s" % ('brand', self.slug), filename)

    logo_image = models.ImageField(
        _('Logo image'),
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    background_image = models.ImageField(
        _('Background image'),
        upload_to=get_upload_path,
        blank=True,
        null=True
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True
    )

    brand_link = models.URLField(blank=True, null=True)
    name = models.CharField(_('Name'), max_length=30)
    main_image = models.ImageField(_('Image'), upload_to=get_upload_path)
    slug = models.SlugField(_('Slug'), unique=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'catalogue:brand_detail', (self.slug, )

    @property
    def get_tags(self):
        tags = Tag.objects.filter(item__brand=self).distinct()
        return tags

    @property
    def get_site_name(self):
        if not self.brand_link:
            domain = urlparse(self.brand_link).netloc.replace('www.', '')
            return domain

        return ''


class Item(models.Model):
    """
    Represent Item
    """
    main_image = models.ImageField(_('Image'), upload_to='items')
    title = models.CharField(_('Title'), max_length=120)
    price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
    link = models.URLField(_('Link'))
    description = models.TextField(_('Description'))
    site_name = models.CharField(
        _('Site name'),
        max_length=30,
        blank=True,
        null=True,
        help_text=_('from field "Slug" site name set auto, '
                    'don\'t fill this field if site name is good for you')
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name=_('Categories'),
        related_name='items'
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name=_('Brand'),
        related_name='items'
    )
    when_created = models.DateTimeField(_('When created'), auto_now_add=True)
    slug = models.SlugField(_('Slug'), unique=True)

    tags = TaggableManager()
    enable = models.BooleanField(_('Enable'), default=True)

    additional_likes = models.IntegerField(_('Additional likes'), default=0)

    objects = ItemManager()

    related_items = models.ManyToManyField(
        'Item',
        through='RelatedItems',
        blank=True,
        verbose_name=_('Related itemd')
    )
    in_trend = models.BooleanField(_('Trend'),default=True)

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
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

    @permalink
    def get_absolute_url(self):
        return 'catalogue:product_detail', (self.slug, )

    @property
    def get_total_likes(self):
        return self.additional_likes + self.likes.count()


class RelatedItems(models.Model):
    """Related items for primary item"""
    primary = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        related_name='primary_recommendations',
        verbose_name=_("Primary product"))
    recommendation = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        verbose_name=_("Recomendation Items"))
    ranking = models.PositiveSmallIntegerField(
        _('Ranking'), default=0,
        help_text=_('Determines order of the products. A product with a higher'
                    ' value will appear before one with a lower ranking.'))

    class Meta:
        ordering = ['primary', '-ranking']
        unique_together = ('primary', 'recommendation')
        verbose_name = _('Product related')
        verbose_name_plural = _('Product related')
