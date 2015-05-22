from __future__ import unicode_literals

import os
import traceback

from django.utils.six.moves import range
from django.utils import timezone
from django.db import transaction, Error

from .signals import export_started, export_completed, \
    import_started, import_completed, error_raised
from .helpers import column_index
from .exceptions import ErrorChoicesMixin

from ..settings import LIMIT_PREVIEW, FILE_PATH


class DataProcessor(object):

    def _set_rows_dimensions(self, preview, import_data):
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

    def _set_cols_dimensions(self, import_data, field_cols):
        if self.settings.start_col:
            start_col_index = column_index(self.settings.start_col)
            if start_col_index > self.start['col']:
                self.start['col'] = start_col_index - 1

                if not import_data:
                    self.end['col'] += self.start['col']

        if field_cols:
            self.end['col'] = self.start['col'] + field_cols

        if self.settings.end_col:
            end_col_index = column_index(self.settings.end_col)

            if end_col_index < self.end['col']:
                self.end['col'] = end_col_index

    def set_dimensions(
            self, start_row, start_col, end_row, end_col, preview=False,
            import_data=False, field_cols=None):
        """Return start, end table dimensions"""

        self.start = {'row': start_row, 'col': start_col}
        self.end = {'row': end_row, 'col': end_col}

        self._set_rows_dimensions(preview, import_data)
        self._set_cols_dimensions(import_data, field_cols)

        self.cells = range(self.start['col'], self.end['col'])
        self.rows = range(self.start['row'], self.end['row'])


class Processor(DataProcessor):

    """Base implementation of import and export operations"""

    position = 0
    file_format = None
    file_description = None

    def __init__(self, settings, manager):
        self.settings = settings
        self.manager = manager
        self.report = None

    def write(self, row, cells=None):
        """Independend write to cell method"""

        raise NotImplementedError

    def read(self, row, cells=None):
        """Independend read from cell method"""

        raise NotImplementedError

    def create(self, path):
        """Create file for given path"""

        raise NotImplementedError

    def open(self, path):
        """Open file for given path"""

        raise NotImplementedError

    def save(self):
        """Save result file"""

        raise NotImplementedError

    def create_export_path(self):
        # TODO: refactor filepath

        filename = '{}{}'.format(
            self.settings.filename or str(self.report.id), self.file_format)
        path = FILE_PATH()(self.report, '', absolute=True)
        if not os.path.exists(path):
            os.makedirs(path)

        return filename, os.path.join(path, filename)

    def write_header(self, data):
        if self.settings.include_header and data['fields']:
            header_data = list(map(
                lambda f: f.name or f.attribute,
                data['fields']))

            self.write(self.start['row'], header_data)

    def export_data(self, data):
        """Export data from queryset to file and return path"""

        # send signal to create report
        for response in export_started.send(self):
            self.report = response[1]

        self.set_dimensions(0, 0, data['rows'], data['cols'])
        filename, path = self.create_export_path()
        self.create(path)

        # write header
        self.write_header(data)

        # write data
        data = data['items']

        for row in self.rows:
            row_data = []

            for col in self.cells:
                row_data.append(next(data))

            self.write(row, row_data)

        self.save()

        # send signal to save report
        for response in export_completed.send(
                self, date=timezone.now(),
                path=FILE_PATH()(self.report, filename)):
            self.report = response[1]

        return self.report

    def _prepare_fk_attrs(self, related_attrs, key, _model):
        key_model, key_attr = key.split('|_fk_|')

        attrs = related_attrs.get(key_model, {})
        attrs[key_attr] = _model[key]
        related_attrs[key_model] = attrs

        return related_attrs

    def _prepare_mtm_attrs(self, related_attrs, key, _model):
        key_model, key_attr = key.split('|_m_|')

        value = _model[key]

        attrs = related_attrs.get(key_model, {})
        attrs[key_attr] = value
        related_attrs[key_model] = attrs

        return related_attrs

    def prepare_attrs(self, _model):
        model_attrs = {}
        related_attrs = {}

        for key in _model.keys():
            if '|_fk_|' in key:
                related_attrs = self._prepare_fk_attrs(
                    related_attrs, key, _model)
            elif '|_m_|' in key:
                related_attrs = self._prepare_mtm_attrs(
                    related_attrs, key, _model)
            else:
                model_attrs[key] = _model[key]

        return model_attrs, related_attrs

    def import_data(self, model, path=None):
        """Import data to model and return errors if exists"""

        path = path or self.settings.buffer_file.path

        # send signal to create report
        for response in import_started.send(self, path=path):
            self.report = response[1]
        self.report.status = self.report.SUCCESS

        data = self.manager.prepare_import_data(self, model)
        params = self.manager.filter_dataset(self.settings) or {}
        action = self.manager.get_or_raise('action', self.settings.data_action)
        context = self.manager.prepare_handlers('before', model, self)

        max_rows, max_cols = self.open(path)
        self.set_dimensions(
            0, 0, max_rows, max_cols,
            import_data=True, field_cols=data['cols'])

        items = data['items']

        for row, _model in items:
            model_attrs, related_attrs = self.prepare_attrs(_model)
            model_attrs.update(**params)

            sid = transaction.savepoint()

            try:
                with transaction.atomic():
                    context = action(
                        model, model_attrs, related_attrs, context,
                        processor=self, path=path, fields=data['fields'],
                        params=params, raw_attrs=_model,
                        mfields=data['mfields'])
            except (Error, ValueError,
                    AttributeError, TypeError, IndexError):

                transaction.savepoint_rollback(sid)
                error_message = traceback.format_exc()
                if 'File' in error_message:
                    error_message = 'File{}'.format(
                        error_message.split('File')[-1])

                value = {
                    'model_attrs': model_attrs,
                    'related_attrs': related_attrs
                }

                error_raised.send(
                    self,
                    error=error_message,
                    position=row,
                    value=value,
                    step=ErrorChoicesMixin.IMPORT_DATA)
                self.report.status = self.report.ERROR

        self.manager.prepare_handlers('after', model, self, context)

        # send signal to save report
        for response in import_completed.send(
                self, date=timezone.now()):
            self.report = response[1]

        return self.report
