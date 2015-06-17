import os

import django

from django.test import TestCase

from mtr.sync.settings import PREFIX, THEME
from mtr.sync.helpers import themed


class ThemedTest(TestCase):

    def setUp(self):
        self.template_name = 'test_template.html'
        self.theme_name = 'testtheme'
        self.version = django.get_version()[:3]

    def test_changing_theme_by_settings(self):
        """Test changing to the new theme and then fallback to default"""

        new_settings = {
            '{}_{}'.format(PREFIX, 'THEME'): self.theme_name
        }

        new_theme_path = os.path.join(
            'mtr', 'sync', self.theme_name, self.template_name)
        default_theme_path = os.path.join(
            'mtr', 'sync', THEME, self.template_name)

        with self.settings(**new_settings):
            self.assertEquals(themed(self.template_name), new_theme_path)

        self.assertEquals(themed(self.template_name), default_theme_path)

        new_theme_path_with_version = os.path.join(
            'mtr', 'sync', os.path.join(self.theme_name, self.version),
            self.template_name)
        default_theme_path_with_version = os.path.join(
            'mtr', 'sync', os.path.join(THEME, self.version),
            self.template_name)

        with self.settings(**new_settings):
            self.assertEquals(
                themed(self.template_name, True),
                new_theme_path_with_version)

        self.assertEquals(
            themed(self.template_name, True),
            default_theme_path_with_version)
