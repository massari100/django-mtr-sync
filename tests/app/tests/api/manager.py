from django.test import TestCase

from mtr.sync.api import Manager, Processor
from mtr.sync.api.processors.xls import XlsProcessor
from mtr.sync.api.exceptions import ProcessorAlreadyExists, \
    ProcessorDoesNotExists
from mtr.sync.models import Settings


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
        self.manager.register('processor', TestProcessor)
        self.assertTrue(self.manager.has_processor(TestProcessor))

        self.manager.unregister('processor', TestProcessor)
        self.assertFalse(self.manager.has_processor(TestProcessor))

    def test_register_already_registered_processor(self):
        self.manager.register('processor', TestProcessor)

        with self.assertRaises(ProcessorAlreadyExists):
            self.manager.register('processor', TestProcessor)

    def test_make_processor_not_exist(self):
        with self.assertRaises(ProcessorDoesNotExists):
            self.manager.make_processor(self.settings)

    def test_processor_ordering(self):
        unordered_processors = [ThirdProcesor, TestProcessor, SecondProcessor]
        for processor in unordered_processors:
            self.manager.register('processor', processor)

        ordered_processors = [TestProcessor, SecondProcessor, ThirdProcesor]
        self.assertEqual(
            list(self.manager.processors.values()), ordered_processors)
