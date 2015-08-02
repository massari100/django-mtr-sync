from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CharNullField(models.CharField):
    description = "CharField that stores NULL but returns empty string"
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, models.CharField):
            return value
        if value is None:
            return ''
        else:
            return value

    def get_prep_value(self, value):
        value = super().get_prep_value(value)

        if not value:
            return None
        else:
            return value


class CreatedAtUpdatedAtMixin(models.Model):
    created_at_in_db = models.DateTimeField(
        _('created at'), auto_now_add=True, null=True)
    created_at = models.DateTimeField(
        _('created at'), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True


class PositionRootMixin(models.Model):
    position = models.PositiveIntegerField(
        _('position'), null=True, blank=True, default=0)

    class Meta:
        abstract = True

        ordering = ('position',)

    def save(self, *args, **kwargs):
        if self.position is None:
            self.position = self.__class__.objects \
                .aggregate(models.Max('position'))['position__max']
            self.position = self.position + 1 if self.position else 1

        super().save(*args, **kwargs)


class PositionRelatedMixin(models.Model):
    POSITION_RELATED_FIELD = None

    position = models.PositiveIntegerField(
        _('position'), null=True, blank=True, default=0)

    class Meta:
        abstract = True

        ordering = ('position',)

    def save(self, *args, **kwargs):
        related_field = getattr(self, self.POSITION_RELATED_FIELD, None)

        if self.position is None and related_field is not None:
            self.position = self.__class__.objects.filter(**{
                self.POSITION_RELATED_FIELD: related_field}) \
                .aggregate(models.Max('position'))['position__max']
            self.position = self.position + 1 if self.position else 1

        super().save(*args, **kwargs)


class TreePositionMixin(models.Model):
    POSITION_PARENT_FIELD = 'parent'

    position = models.PositiveIntegerField(
        _('position'), null=True, blank=True, default=0)

    class Meta:
        abstract = True

        ordering = ('position',)

    def save(self, *args, **kwargs):
        if self.position is None:
            parent = getattr(self, self.POSITION_PARENT_FIELD, None)
            if parent is None:
                self.position = self.__class__.objects
            else:
                self.position = self.__class__.objects \
                    .filter(**{self.POSITION_PARENT_FIELD: parent})
            self.position = self.position \
                .aggregate(models.Max('position'))['position__max']
            self.position = self.position + 1 if self.position else 0

        super().save(*args, **kwargs)
