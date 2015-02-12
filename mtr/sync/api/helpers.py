from django.db import models


def get_models():
    model_list = filter(
        lambda m: getattr(m, 'ignore_sync', True), models.get_models())
    # model_list = filter(
    #     lambda m: str(m.__module__) not in ['django', 'mtr.sync'])
    return model_list


def model_choices():
    """Return all registered django models as choices"""

    for model in get_models():
        yield (model.__module__, model._meta.verbose_name)
