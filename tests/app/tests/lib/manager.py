from django.test import TestCase

from mtr.sync.tests import SyncTestMixin
from mtr.sync.lib import Processor
from mtr.sync.lib.processors.xls import XlsProcessor

from ...models import Person, Office, Tag


class TestProcessor(Processor):
    pass


class SecondProcessor(Processor):
    position = 1


class ThirdProcesor(Processor):
    position = 2


class ProcessorTest(SyncTestMixin, TestCase):
    MODEL = Person
    RELATED_MODEL = Office
    RELATED_MANY = Tag
    PROCESSOR = XlsProcessor
    CREATE_PROCESSOR_AT_SETUP = False

    def test_value_manipulation_converters(self):
        # self.manager.register('processor', item=self.PROCESSOR)
        self.processor = self.manager.make_processor(self.settings)
        self.fields = self.settings.create_default_fields()

        before_data = list(self.manager.prepare_export_data(
            self.processor, self.queryset)['items'])

        @self.manager.register('converter', label='multiply by 10')
        def test_filter(value, field, action):
            return value * 10

        for field in self.fields:
            if field.attribute == 'id':
                field.processors = 'test_filter,'

        after_data = self.manager.prepare_export_data(
            self.processor, self.queryset)['items']

        data_counter = 0
        for before_item, after_item in zip(before_data, after_data):
            if data_counter % 1:
                self.assertEqual(before_item, after_item / 10)
            data_counter += 1
