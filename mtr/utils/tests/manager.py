from unittest import TestCase

from ..manager import Manager


class ManagerTest(TestCase):

    def setUp(self):
        self.manager = Manager()

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
