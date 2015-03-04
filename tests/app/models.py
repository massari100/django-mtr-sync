import random

from django.utils.encoding import python_2_unicode_compatible
from django.utils.six.moves import range
from django.db import models


@python_2_unicode_compatible
class Office(models.Model):
    office = models.CharField('office', max_length=255)
    address = models.CharField('address', max_length=255)

    def __str__(self):
        return self.office

    class Meta:
        verbose_name = 'office'
        verbose_name_plural = 'offices'


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField('tag', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


@python_2_unicode_compatible
class Person(models.Model):
    name = models.CharField('name', max_length=255)
    surname = models.CharField('surname', max_length=255)
    gender = models.CharField('gender', max_length=255, choices=(
        ('M', 'Male'),
        ('F', 'Female'),
    ))
    security_level = models.PositiveIntegerField('security level')
    some_excluded_field = models.DecimalField('some decimal',
        max_digits=10, decimal_places=3, null=True)

    office = models.ForeignKey(Office, null=True, blank=True)
    # tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = 'person'
        verbose_name_plural = 'persons'

    def populate(self, num=100):
        for i in range(num):
            name = list(self.name)
            random.shuffle(name)
            name = ''.join(name)

            surname = list(self.surname)
            random.shuffle(surname)
            surname = ''.join(surname)

            self.__class__.objects.create(
                name=name,
                surname=surname,
                gender=random.choice(['M', 'F']),
                security_level=random.choice(range(100))
            )

    @property
    def custom_method(self):
        return '{}-{}'.format(self.name, self.surname)

    @custom_method.setter
    def custom_method(self, value):
        self.name, self.surname = value.split('-')

    def __str__(self):
        return self.name

    sync_settings = {
        'fields': ['custom_method'],
        'exclude': ['some_excluded_field']
    }
