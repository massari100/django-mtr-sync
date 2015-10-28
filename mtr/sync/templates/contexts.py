from ..models import Settings


def settings_for_model():
    Settings.objects.filter(show_in_quicklist=True)
