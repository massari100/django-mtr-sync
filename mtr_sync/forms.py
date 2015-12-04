from django import forms

from ..utils.forms import GlobalInitialFormMixin

from .models import Settings


class SettingsAdminForm(GlobalInitialFormMixin, forms.ModelForm):

    class Meta:
        exclude = []
        model = Settings
