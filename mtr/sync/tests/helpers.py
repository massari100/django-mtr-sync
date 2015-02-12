import os

from django.test import TestCase

from ..settings import PREFIX, THEME_PATH
from ..helpers import themed


class ThemedTest(TestCase):

    def setUp(self):
        self.template_name = 'test_template.html'
        self.theme_name = 'testtheme'

    def test_changing_theme_by_settings(self):
        """Test changing to the new theme and then fallback to default"""

        new_settings = {
            '{}_{}'.format(PREFIX, 'THEME_PATH'): self.theme_name
        }

        new_theme_path = os.path.join(
            'mtr', 'sync', self.theme_name, self.template_name)
        default_theme_path = os.path.join(
            'mtr', 'sync', THEME_PATH(), self.template_name)

        with self.settings(**new_settings):
            self.assertEquals(themed(self.template_name), new_theme_path)

        self.assertEquals(themed(self.template_name), default_theme_path)
