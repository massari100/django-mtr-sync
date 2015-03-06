from django.test import TestCase

from mtr.sync.tests import ApiTestMixin
from mtr.sync.api import Processor
from mtr.sync.api.processors.xls import XlsProcessor
from mtr.sync.api.exceptions import ItemAlreadyRegistered, \
    ItemDoesNotRegistered
from mtr.sync.models import Filter, FilterParams

from ...models import Person, Office


class TestProcessor(Processor):
    pass


class SecondProcessor(Processor):
    position = 1


class ThirdProcesor(Processor):
    position = 2


class ManagerTest(ApiTestMixin, TestCase):
    MODEL = Person
    RELATED_MODEL = Office
    PROCESSOR = XlsProcessor
    CREATE_PROCESSOR_AT_SETUP = False

    def test_registering_and_unregistering_processor(self):
        self.manager.register('processor', TestProcessor)
        self.assertTrue(self.manager.has('processor', TestProcessor))

        self.manager.unregister('processor', TestProcessor)
        self.assertFalse(self.manager.has('processor', TestProcessor))

    def test_register_already_registered_processor(self):
        self.manager.register('processor', TestProcessor)

        with self.assertRaises(ItemAlreadyRegistered):
            self.manager.register('processor', TestProcessor)

    def test_make_processor_not_exist(self):
        with self.assertRaises(ItemDoesNotRegistered):
            self.manager.make_processor(self.settings)

    def test_processor_ordering(self):
        unordered_processors = [ThirdProcesor, TestProcessor, SecondProcessor]
        for processor in unordered_processors:
            self.manager.register('processor', processor)

        ordered_processors = [TestProcessor, SecondProcessor, ThirdProcesor]
        self.assertEqual(
            list(self.manager.processors.values()), ordered_processors)

    def test_registering_dict_instance_attributes(self):
        @self.manager.register('filter', name='test')
        def some_filter():
            return None

        self.assertEqual(
            list(self.manager.filters.keys())[0], 'test')
        self.assertEqual(
            list(self.manager.filters.values())[0], some_filter)

        self.assertEqual(
            self.manager.unregister('filter', 'test'), 'test')
        self.assertEqual(self.manager.filters, {})

    def test_value_manipulation_filters(self):
        self.manager.register('processor', self.PROCESSOR)
        self.processor = self.manager.make_processor(self.settings)
        self.fields = self.settings.create_default_fields()

        before_data = list(self.manager.prepare_export_data(
            self.processor, self.queryset)['items'])

        @self.manager.register('filter', label='multiply by 10')
        def test_filter(value, field, action):
            return value * 10

        filter_related = Filter.objects.get(name='test_filter')
        for field in self.fields:
            if field.attribute == 'id':
                field_related = field
                break

        FilterParams.objects.create(
            filter_related=filter_related, field_related=field_related)

        after_data = self.manager.prepare_export_data(
            self.processor, self.queryset)['items']

        data_counter = 0
        for before_item, after_item in zip(before_data, after_data):
            if data_counter % 1:
                self.assertEqual(before_item, after_item / 10)
            data_counter += 1

    def test_model_attributes(self):
        fields = self.manager.model_attributes(self.settings)
        fields = list(map(lambda f: f[0], fields))

        self.assertEqual([
            'id', 'name', 'surname', 'gender', 'security_level',
            'office.id', 'office.office', 'office.address',
            'tags.id', 'tags.name',
            'custom_method'], fields)

    def test_process_attribute(self):
        self.assertEqual(
            self.manager.process_attribute(
                self.instance, 'name'), self.instance.name)
        self.assertEqual(
            self.manager.process_attribute(
                self.instance, 'office.address'), self.instance.office.address)
        self.assertEqual(
            self.manager.process_attribute(
                self.instance, 'notexist'), None)
        self.assertEqual(
            self.manager.process_attribute(
                self.instance, 'office.notexist.attr'), None)
