from django.test import TestCase

from mtr.sync.api.helpers import column_name, column_index, column_value


class HelpersTest(TestCase):

    def test_column_index_value_transform(self):
        self.assertEqual(column_name(0), 'A')
        self.assertEqual(column_name(25), 'Z')

        self.assertEqual(column_value(10), 10)
        self.assertEqual(column_value('A'), 0)

        self.assertEqual(column_index('A'), 0)
        self.assertEqual(column_index('Z'), 25)
