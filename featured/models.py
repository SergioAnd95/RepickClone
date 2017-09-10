from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink


class Issue(models.Model):
    """
    Represent Issue
    """
    when_created = models.DateTimeField(_('Created date'), auto_now_add=True)
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'))
    slug = models.SlugField(_('Slug'), unique=True)
    main_image = models.ImageField(_('Main image'), upload_to='issue')

    def __str__(self):
        return _('Issue: %s #%d' % (self.title, self.id))

    class Meta:
        verbose_name=_('Issue')
        verbose_name_plural=_('Issues')

    @permalink
    def get_absolute_url(self):
        return 'featured:issue_detail', (self.slug, )


class IssueRaw(models.Model):
    """
    Represent raw of issue
    """
    class DisplayType:
        JOIN = 1
        SEPARATED = 2

        DISPLAY_CHOICES = (
            (SEPARATED, _('Separated')),
            (JOIN, _('Join'))
        )

    class SizeType:
        SMALL = 'small'
        MEDIUM = 'medium'
        LARGE = 'large'
        EXTRALARGE = 'extralarge'

        SIZE_CHOICES = (
            (SMALL, _('Small')),
            (MEDIUM, _('Medium')),
            (LARGE, _('Large')),
            (EXTRALARGE, _('Extralarge'))
        )

    class CellCountType:
        ONE_SLOT = 1
        TWO_SLOT = 2
        THREE_SLOT = 3
        FOUR_SLOT = 4
        BIG_AND_SMALL = 5
        SMALL_AND_BIG = 6

        COUNT_CHOICES = (
            (ONE_SLOT, _('One slot')),
            (TWO_SLOT, _('Two slots')),
            (THREE_SLOT, _('Three slots')),
            (FOUR_SLOT, _('Four slots')),
            (BIG_AND_SMALL, _('Big and small')),
            (SMALL_AND_BIG, _('Small and big'))
        )

    position = models.PositiveIntegerField(_('Position'), default=0)
    issue = models.ForeignKey(Issue, related_name='raws', verbose_name=_('Issue'))
    display_type = models.PositiveSmallIntegerField(
        _('Display type'),
        choices=DisplayType.DISPLAY_CHOICES,
        default=DisplayType.JOIN
    )
    size = models.CharField(
        _('Size'),
        max_length=10,
        choices=SizeType.SIZE_CHOICES,
        default=SizeType.SMALL
    )
    cell_counts = models.PositiveIntegerField(
        _('Cells counts'),
        choices=CellCountType.COUNT_CHOICES,
        default=CellCountType.ONE_SLOT
    )

    def __str__(self):
        return '%d %s'%(self.position, self.issue)

    class Meta:
        verbose_name = _('Issue Raw')
        verbose_name_plural = _('Issue Raws')
        ordering = ('issue', 'position')


class IssueCell(models.Model):
    """
    Represent cell of issue raw
    """
    class ContentType:
        ITEM = 1
        IMAGE = 2

        TYPE_CHOICES = (
            (ITEM, _('Item')),
            (IMAGE, _('Image'))
        )
    position = models.PositiveIntegerField(
        _('Position'),
        default=0
    )
    issue_raw = models.ForeignKey(
        IssueRaw,
        related_name='cells',
        verbose_name=('Issue raw')
    )
    content_type = models.PositiveSmallIntegerField(
        _('Content type'),
        choices=ContentType.TYPE_CHOICES,
        default=ContentType.ITEM
    )
    item = models.ForeignKey(
        'catalogue.Item',
        verbose_name=_('Item'),
        blank=True,
        null=True
    )
    image = models.ImageField(
        _('Image'),
        upload_to='issue',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Issue cell')
        verbose_name_plural = _('Issue cells')
        ordering = ('issue_raw', 'position')