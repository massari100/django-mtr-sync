from django.test import TestCase

from mtr.sync.tests import ApiTestMixin
from mtr.sync.lib import Processor
from mtr.sync.lib.processors.xls import XlsProcessor

from ...models import Person, Office, Tag


class TestProcessor(Processor):
    pass


class SecondProcessor(Processor):
    position = 1


class ThirdProcesor(Processor):
    position = 2


class ManagerTest(ApiTestMixin, TestCase):
    MODEL = Person
    RELATED_MODEL = Office
    RELATED_MANY = Tag
    PROCESSOR = XlsProcessor
    CREATE_PROCESSOR_AT_SETUP = False

    def test_registering_and_unregistering_processor(self):
        self.manager.register('processor', item=TestProcessor)
        self.assertTrue(self.manager.has('processor', TestProcessor))

        self.manager.unregister('processor', TestProcessor)
        self.assertFalse(self.manager.has('processor', TestProcessor))

    def test_register_already_registered_processor(self):
        self.manager.register('processor', item=TestProcessor)

        with self.assertRaises(ValueError):
            self.manager.register('processor', item=TestProcessor)

    def test_make_processor_not_exist(self):
        with self.assertRaises(ValueError):
            self.manager.make_processor(self.settings)

    def test_processor_ordering(self):
        unordered_processors = [ThirdProcesor, TestProcessor, SecondProcessor]
        for processor in unordered_processors:
            self.manager.register('processor', item=processor)

        ordered_processors = [TestProcessor, SecondProcessor, ThirdProcesor]
        self.assertEqual(
            list(self.manager.processors.values()), ordered_processors)

    def test_registering_dict_instance_attributes(self):
        old_converters = self.manager.converters.copy()

        @self.manager.register('converter', name='test')
        def some_filter():
            return None

        self.assertIn('test', self.manager.converters.keys())
        self.assertIn(some_filter, self.manager.converters.values())

        self.assertEqual(self.manager.unregister('converter', 'test'), 'test')
        self.assertEqual(
            list(self.manager.converters.keys()), list(old_converters.keys()))

    def test_value_manipulation_converters(self):
        self.manager.register('processor', item=self.PROCESSOR)
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
