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

    def test_settings_modified_by_link(self):
        content = self.client.get(
            '{}?action=export&model=person&app=app'.format(
                reverse('admin:mtrsync_settings_add')))

        # TODO: more checks

        form = content.context['adminform'].form

        self.assertEqual(form.fields['action'].initial, 0)
