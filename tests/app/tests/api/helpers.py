from django.test import TestCase

from mtr.sync.api.helpers import column_name, column_index, column_value, \
    model_attributes, process_attribute
from mtr.sync.tests import ApiTestMixin
from mtr.sync.api.processors import csv

from ...models import Person, Office, Tag


class HelpersTest(ApiTestMixin, TestCase):
    MODEL = Person
    RELATED_MODEL = Office
    RELATED_MANY = Tag
    PROCESSOR = csv.CsvProcessor

    def test_column_index_value_transform(self):
        self.assertEqual(column_name(0), 'A')
        self.assertEqual(column_name(25), 'Z')

        self.assertEqual(column_value(10), 10)
        self.assertEqual(column_value('A'), 0)

        self.assertEqual(column_index('A'), 0)
        self.assertEqual(column_index('Z'), 25)

    def test_model_attributes(self):
        fields = model_attributes(self.settings)
        fields = list(map(lambda f: f[0], fields))

        self.assertEqual([
            'id', 'name', 'name_de', 'name_en',
            'surname', 'surname_de', 'surname_en', 'gender', 'security_level',
            'office|_fk_|id', 'office|_fk_|office', 'office|_fk_|address',
            'tags|_m_|id', 'tags|_m_|name',
            'custom_method', 'none_param'], fields)

    def test_process_attribute(self):
        self.assertEqual(
            process_attribute(
                self.instance, 'name'), self.instance.name)
        self.assertEqual(
            process_attribute(
                self.instance, 'office|_fk_|address'),
            self.instance.office.address)
        self.assertEqual(
            process_attribute(
                self.instance, 'notexist'), None)
        self.assertEqual(
            process_attribute(
                self.instance, 'office|_fk_|notexist|_fk_|attr'), None)
