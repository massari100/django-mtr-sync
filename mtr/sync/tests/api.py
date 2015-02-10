from django.test import TestCase

from ..api import Manager, Processor
from ..processors import XlsProcessor
from ..models import Settings


class TestProcessor(Processor):
    pass


class ManagerTest(TestCase):
    def setUp(self):
        self.manager = Manager.create()
        self.manager.register(XlsProcessor)

        # don't creating settings in database just simulate
        # passed data from view of modelform
        self.settings = Settings(processor=XlsProcessor.__name__)

    def test_registering_and_unregistering_processor(self):
        self.manager.register(XlsProcessor)
        self.assertEqual(self.manager.has_processor(TestProcessor), True)

        self.manager.unregister(XlsProcessor)
        self.assertEqual(self.manager.has_processor(TestProcessor), False)

    def test_export_data_and_report_generation(self):
        report = self.manager.export_data(**{
            'processor': self.settings.processor,
            'main_model': None
        })

        # self.assertEqual()
