from django import forms

from .models import Settings


class SettingsAdminForm(forms.ModelForm):
    INITIAL = {}

    def __init__(self, *args, **kwargs):
        if kwargs.get('initial', None):
            kwargs['initial'].update(self.INITIAL)

        super(SettingsAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        exclude = []
        model = Settings
