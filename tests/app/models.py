import random

from django.utils.encoding import python_2_unicode_compatible
from django.utils.six.moves import range
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

    def __str__(self):
        return self.name
