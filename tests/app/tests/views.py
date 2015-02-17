from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from mtr.sync.helpers import themed


class DashboardPageTest(TestCase):

    def setUp(self):
        self.password = 'admin_password'
        self.user = User.objects.create_superuser(
            'admin', 'admin', password=self.password)
        self.client.login(username=self.user.username, password=self.password)

    def test_display_last_reports_default_admin(self):
        response = self.client.get(reverse('mtr.sync:dashboard'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, themed('dashboard.html'))
