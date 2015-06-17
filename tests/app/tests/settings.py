from django.test import TestCase

from mtr.sync.settings import FILE_PATH


class MockInstance(object):
    action = 1


class SettingsTest(TestCase):

    def test_default_filepath_name(self):
        new_settings = {
            'MEDIA_ROOT': '/some/path/'
        }
        instance = MockInstance()

        with self.settings(**new_settings):
            self.assertEqual(
                FILE_PATH(instance, 'filename.xls'),
                'sync/import/filename.xls')
