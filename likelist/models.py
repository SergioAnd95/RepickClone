from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class LikeList(models.Model):
    when_created = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name_plural = _('Списки понравившегось')
        verbose_name = _('Список понравившегось')

    def add_item(self, item):
        likes = self.likes.filter(item=item)
        if likes.count() == 0:
            self.likes.create(item=item)

    def remove_item(self, item):
        self.likes.filter(item=item).delete()

    def exist_item(self, item):
        return self.likes.filter(item=item).count() > 0


class Like(models.Model):
    like_list = models.ForeignKey(
        LikeList,
        verbose_name=_('Список понравившегось'),
        related_name='likes'
    )
    item = models.ForeignKey(
        'catalogue.Item',
        verbose_name=_('Товар'),
        related_name='likes'
    )

    when_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('like_list', 'item'))