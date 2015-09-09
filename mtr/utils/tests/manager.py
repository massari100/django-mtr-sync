from unittest import TestCase

from ..manager import BaseManager

manager = BaseManager()


class ManagerTest(TestCase):

    def setUp(self):
        self.manager = BaseManager()

    def test_register_unregister_simple(self):
        @self.manager.register('item')
        def somefunc(some, args):
            print(some, args)

        self.assertIn(somefunc.__name__, self.manager._registered['item'])
        self.assertIn(somefunc, self.manager._registered['item'].values())

        with self.assertRaises(ValueError):
            self.manager.register('item', item=somefunc)

        self.manager.unregister('item', somefunc)

        self.assertNotIn(somefunc.__name__, self.manager._registered['item'])
        self.assertNotIn(somefunc, self.manager._registered['item'].values())

    def test_register_unregister_custom_params(self):
        @self.manager.register('item', name='test')
        def somefunc(some, args):
            print(some, args)

        self.assertIn('test', self.manager._registered['item'])
        self.assertIn(somefunc, self.manager._registered['item'].values())

        self.manager.unregister('item', 'test')

        self.assertNotIn('test', self.manager._registered['item'])
        self.assertNotIn(somefunc, self.manager._registered['item'].values())

    def test_register_unregister_inner(self):
        @self.manager.register('item', related='asd')
        def somefunc(some, args):
            print(some, args)

        @self.manager.register('item', name='other', related='asd')
        def someotherfunc(some, args):
            print(some, args)

        self.assertIn(
            somefunc.__name__, self.manager._registered['item']['asd'])
        self.assertIn(
            somefunc, self.manager._registered['item']['asd'].values())

        self.assertIn('other', self.manager._registered['item']['asd'])
        self.assertIn(
            someotherfunc, self.manager._registered['item']['asd'].values())

        self.assertEqual(
            somefunc, self.manager.get('item', 'somefunc', related='asd'))
        self.assertEqual(
            someotherfunc, self.manager.get('item', 'other', related='asd'))

        self.manager.unregister('item', somefunc, related='asd')

        self.assertNotIn('test', self.manager._registered['item']['asd'])
        self.assertNotIn(
            somefunc, self.manager._registered['item']['asd'].values())

    def test_import_modules(self):
        self.manager.import_modules(('mtr.utils.tests.testmodule:manager',))
        self.assertIn('item', self.manager._registered.keys())
        self.assertIn('request', self.manager._registered.keys())
