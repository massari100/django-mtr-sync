from __future__ import unicode_literals

import os

from django.utils.six.moves import range
from django.utils.encoding import smart_text
from django.utils import timezone
from django.db import models, transaction, Error

from .signals import export_started, export_completed, \
    import_started, import_completed
from .helpers import column_value, model_fields
from ..settings import LIMIT_PREVIEW, FILE_PATH


class Processor(object):

    """Base implementation of import and export operations"""

    # TODO: add managing none fields

    position = 0
    file_format = None
    file_description = None

    def __init__(self, settings, manager):
        self.settings = settings
        self.manager = manager
        self.report = None

    def write(self, row, value, cells=None):
        """Independend write to cell method"""

        raise NotImplementedError

    def read(self, row, value, cells=None):
        """Independend read from cell method"""

        raise NotImplementedError

    def _set_rows_dimensions(self, preview=False, import_data=False):
        if self.settings.start_row and \
                self.settings.start_row > self.start['row']:
            self.start['row'] = self.settings.start_row - 1

            if not import_data:
                self.end['row'] += self.start['row']

        if self.settings.end_row and \
                self.settings.end_row < self.end['row']:
            self.end['row'] = self.settings.end_row

        limit = LIMIT_PREVIEW()
        if preview and limit < self.end['row']:
            self.end['row'] = limit + self.start['row'] - 1

        if self.settings.include_header:
            if import_data:
                self.start['row'] += 1
            else:
                self.start['row'] += 1
                self.end['row'] += 1

    def _set_cols_dimensions(self, import_data=False):
        if self.settings.start_col:
            start_col_index = column_value(self.settings.start_col)
            if start_col_index > self.start['col']:
                self.start['col'] = start_col_index - 1

                if not import_data:
                    self.end['col'] += self.start['col']

        if self.settings.end_col:
            end_col_index = column_value(self.settings.end_col)

            if end_col_index < self.end['col']:
                self.end['col'] = end_col_index

    def set_dimensions(
            self, start_row, start_col, end_row, end_col, preview=False,
            import_data=False):
        """Return start, end table dimensions"""

        self.start = {'row': start_row, 'col': start_col}
        self.end = {'row': end_row, 'col': end_col}

        self._set_rows_dimensions(preview, import_data)
        self._set_cols_dimensions(import_data)

        self.cells = range(self.start['col'], self.end['col'])
        self.rows = range(self.start['row'], self.end['row'])

    def export_data(self, data):
        """Export data from queryset to file and return path"""

        # send signal to create report
        for response in export_started.send(self.__class__, processor=self):
            self.report = response[1]

        self.set_dimensions(0, 0, data['rows'], data['cols'])

        # save external file and report
        path = FILE_PATH()(self.report, '')
        if not os.path.exists(path):
            os.makedirs(path)

        filename = '{}{}'.format(
            self.settings.filename or str(self.report.id), self.file_format)

        path = os.path.join(path, filename)

        # create export file for write
        self.create(path)

        # write header
        if self.settings.include_header and data['fields']:
            header_data = list(map(
                lambda f: f.name or f.get_attribute_display(),
                data['fields']))

            self.write(self.start['row'], header_data)

        # write data
        data = data['items']

        for row in self.rows:
            row_data = []

            for col in self.cells:
                row_data.append(next(data))

            self.write(row, row_data)

        self.save()

        if self.settings.id:
            self.report.settings = self.settings

        # send signal to save report
        for response in export_completed.send(
                self.__class__, report=self.report,
                date=timezone.now(),
                path=FILE_PATH()(self.report, filename, relative=True)):
            self.report = response[1]

        return self.report

    def process_instances(self, _model, model):
        """Process instances (create, update, delete) for given params"""

        main_model_attrs = {}
        related_models = {}
        # TODO: sub-fields
        # TODO: update if, create if, delete if

        for key in _model['attrs'].keys():
            if '|_fk_|' in key:
                key_model, key_attr = key.split('|_fk_|')

                attrs = related_models.get(key_model, {})
                attrs[key_attr] = _model['attrs'][key]
                related_models[key_model] = attrs
            # elif '|_m_|' in key:
            #     key_model, key_attr = key.split('|_m_|')

            #     value = _model['attrs'][key]

            #     attrs = related_models.get(key_model, {})
            #     attrs[key_attr] = value
            #     related_models[key_model] = attrs
            else:
                main_model_attrs[key] = _model['attrs'][key]

        instance = model(**main_model_attrs)
        fields = model_fields(model)

        # TODO: refactor many to many attrs

        for key in related_models.keys():
            related_field = fields.get(key)
            related_model = related_field.rel.to

            if isinstance(related_field, models.ForeignKey):
                related_instance = related_model(**related_models[key])
                related_instance.save()

                setattr(instance, key, related_instance)
            # elif isinstance(related_field, models.ManyToManyField):
            #     instance_attrs = []
            #     rel_values = list(related_models[key].values())
            #     indexes = len(rel_values[0].split(','))

            #     for index in range(indexes):
            #         instance_values = {}
            #         for k in related_models[key].keys():
            #             value = related_models[key][k] \
            #                 .split(',')[index]
            #             if value.isdigit():
            #                 value = int(value)
            #             instance_values[k] = value
            #     instance_attrs.append(instance_values)

            #     for instance_attr in instance_attrs:
            #         items = getattr(instance, key)
            #         instance_attr.pop('id', None)
            #         items.create(**instance_attr)

        instance.save()

    def import_data(self, model, path=None):
        """Import data to model and return errors if exists"""

        path = path or self.settings.buffer_file.path

        # send signal to create report
        for response in import_started.send(self.__class__, processor=self,
                path=path):
            self.report = response[1]

        # open file and set dimensions
        max_rows, max_cols = self.open(path)
        self.set_dimensions(0, 0, max_rows, max_cols, import_data=True)

        rows = (self.read(row) for row in self.rows)
        data = self.manager.prepare_import_data(self, rows)

        with transaction.atomic():
            for _model in data:
                sid = transaction.savepoint()

                try:
                    with transaction.atomic():
                        self.process_instances(_model, model)
                except (Error, ValueError):
                    transaction.savepoint_rollback(sid)

            transaction.savepoint_commit(sid)

        if self.settings.id:
            self.report.settings = self.settings

        # send signal to save report
        for response in import_completed.send(
                self.__class__, report=self.report,
                date=timezone.now()):
            self.report = response[1]

        return self.report
