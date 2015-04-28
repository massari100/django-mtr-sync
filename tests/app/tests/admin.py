from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class AdminMixinTest(TestCase):

    def setUp(self):
        self.password = 'admin_password'
        self.user = User.objects.create_superuser(
            'admin', 'admin', password=self.password)
        self.client.login(username=self.user.username, password=self.password)

    def test_mixin_has_buttons_in_change_view(self):
        content = self.client.get(reverse('admin:app_person_changelist'))

        self.assertIn('mtr/sync/default/admin/change_list.html',
            map(lambda t: t.name, content.templates))

        self.assertContains(content, 'Export')
        self.assertContains(content, 'Import')

    def test_settings_export_import_modified_by_link(self):
        content = self.client.get(
            '{}?action=export&model=app.person'.format(
                reverse('admin:mtr_sync_settings_add')))
        form = content.context['adminform'].form

        self.assertEqual(form.initial['action'], 0)
        self.assertEqual(form.initial['model'], 'app.person')
        self.assertEqual(form.initial['create_fields'], True)

        content = self.client.get(
            '{}?action=import&model=app.person'.format(
                reverse('admin:mtr_sync_settings_add')))
        form = content.context['adminform'].form

        self.assertEqual(form.initial['action'], 1)
        self.assertEqual(form.initial['model'], 'app.person')
        self.assertEqual(form.initial['create_fields'], False)
        self.assertEqual(form.initial['populate_from_file'], True)
