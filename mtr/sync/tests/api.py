from django.test import TestCase

from mtr.sync.api import Manager, Processor


class TestProcessor(Processor):
    pass


class ApiTest(TestCase):
    def setUp(self):
        self.manager = Manager.create()

    def test_registering_and_unregistering_processor(self):
        self.manager.register(TestProcessor)
        self.assertEqual(self.manager.has_processor(TestProcessor), True)

        self.manager.unregister(TestProcessor)
        self.assertEqual(self.manager.has_processor(TestProcessor), False)
