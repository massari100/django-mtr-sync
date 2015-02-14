from django.utils.encoding import python_2_unicode_compatible

from django.db import models


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField('name', max_length=255)
    surname = models.CharField('surname', max_length=255)
    gender = models.CharField('gender', max_length=255, choices=(
        ('M', 'Male'),
        ('F', 'Female'),
    ))
    security_level = models.PositiveIntegerField('security level')

    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'persons'

    def __str__(self):
        return self.name
