from django.test import TestCase

from mtr.sync.lib.helpers import column_name, column_index, \
    model_attributes, process_attribute, cell_value
from mtr.sync.tests import SyncTestMixin
from mtr.sync.lib.processors import csv

from ...models import Person, Office, Tag


class HelpersTest(SyncTestMixin, TestCase):
    MODEL = Person
    RELATED_MODEL = Office
    RELATED_MANY = Tag
    PROCESSOR = csv.CsvProcessor

    def test_column_index_value_transform(self):
        self.assertEqual(column_name(0), 'A')
        self.assertEqual(column_name(25), 'Z')

        self.assertEqual(column_index(10), 10)
        self.assertEqual(column_index('A'), 0)

    def test_row_values_from_col(self):
        cols = ['1', '2', '3', '4', '5']

        self.assertEqual(cell_value(cols, 0), cols[0])
        self.assertEqual(cell_value(cols, 'A'), cols[0])
        self.assertEqual(cell_value(cols, '4'), cols[4])

        self.assertEqual(cell_value(cols, 'A-C'), cols[:3])
        self.assertEqual(cell_value(cols, 'A-C,B'), cols[:3] + [cols[1]])
        self.assertEqual(
            cell_value(cols, 'A,B,D|'), ' '.join(cols[:2] + [cols[3]]))
        self.assertEqual(
            cell_value(cols, 'A-D,A-F,B|'), ' '.join(
                cols[:4] + cols[:5] + [cols[1]]))
        self.assertEqual(
            cell_value(cols, 'A-D,B|+A-D,B|'), [
                ' '.join(cols[:4] + [cols[1]]),
                ' '.join(cols[:4] + [cols[1]])
            ])

    def test_model_attributes(self):
        fields = model_attributes(self.settings)
        fields = [f[0] for f in fields]

        self.assertEqual([
            'id', 'name', 'surname', 'gender', 'security_level',
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
