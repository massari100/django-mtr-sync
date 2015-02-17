import os
import datetime

from django.test import TestCase
from django.utils.six.moves import range

from ...api import Manager, Processor
from ...api.processors.xls import XlsProcessor
from ...api.exceptions import ProcessorAlreadyExists, ProcessorDoesNotExists
from ...models import Settings


class TestProcessor(Processor):
    pass


class SecondProcessor(Processor):
    position = 1


class ThirdProcesor(Processor):
    position = 2


class ManagerTest(TestCase):
    def setUp(self):
        self.manager = Manager()
        self.settings = Settings(
            processor=XlsProcessor.__name__, worksheet='test')

    def test_registering_and_unregistering_processor(self):
        self.manager.register(TestProcessor)
        self.assertTrue(self.manager.has_processor(TestProcessor))

        self.manager.unregister(TestProcessor)
        self.assertFalse(self.manager.has_processor(TestProcessor))

    def test_register_already_registered_processor(self):
        self.manager.register(TestProcessor)

        with self.assertRaises(ProcessorAlreadyExists):
            self.manager.register(TestProcessor)

    def test_make_processor_not_exist(self):
        with self.assertRaises(ProcessorDoesNotExists):
            self.manager.make_processor(self.settings)

    def test_processor_ordering(self):
        unordered_processors = [ThirdProcesor, TestProcessor, SecondProcessor]
        for processor in unordered_processors:
            self.manager.register(processor)

        ordered_processors = [TestProcessor, SecondProcessor, ThirdProcesor]
        self.assertEqual(self.manager.processors.values(), ordered_processors)

    def test_export_data_and_report_generation(self):
        self.manager.register(XlsProcessor)
        data = {
            'fields': [],
            'rows': 10,
            'cols': 2,
            'items': iter(range(0, 2*10))
        }
        report = self.manager.export_data(self.settings, data)

        # report generated
        self.assertEqual(report.status, report.SUCCESS)
        self.assertEqual(report.action, report.EXPORT)
        self.assertIsInstance(report.completed_at, datetime.datetime)

        # file saved
        self.assertTrue(os.path.exists(report.buffer_file.path))
        self.assertTrue(os.path.getsize(report.buffer_file.path) > 0)
        self.assertIsNone(os.remove(report.buffer_file.path))
