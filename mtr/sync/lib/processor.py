from __future__ import unicode_literals

import os
import traceback

from django.utils.six.moves import range
from django.utils import timezone
from django.db import transaction, Error
from django.core.exceptions import ValidationError

from .signals import export_started, export_completed, \
    import_started, import_completed, error_raised
from .exceptions import ErrorChoicesMixin

from ..settings import SETTINGS


class DataProcessor(object):

    def _set_rows_dimensions(self, import_data):
        if self.settings.start_row and \
                self.settings.start_row > self.start['row']:
            self.start['row'] = self.settings.start_row - 1

            if not import_data:
                self.end['row'] += self.start['row']

        if self.settings.end_row and \
                self.settings.end_row < self.end['row']:
            self.end['row'] = self.settings.end_row

        if self.settings.include_header:
            if import_data:
                self.start['row'] += 1
            else:
                self.start['row'] += 1
                self.end['row'] += 1

    def set_dimensions(
            self, start_row, end_row, end_cols,
            import_data=False, field_cols=None):
        """Return start, end table dimensions"""

        self.start = {'row': start_row}
        self.end = {'row': end_row}

        self._set_rows_dimensions(import_data)

        self.rows = range(self.start['row'], self.end['row'])
        self.cells = range(0, end_cols)


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
        path = SETTINGS['FILE_PATH'](self.report, '', absolute=True)
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

        self.set_dimensions(0, data['rows'], data['cols'])
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
                path=SETTINGS['FILE_PATH'](self.report, filename)):
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

        if self.settings.buffer_file:
            path = self.settings.buffer_file.path

        # send signal to create report
        for response in import_started.send(self, path=path):
            self.report = response[1]
        self.report.status = self.report.SUCCESS

        data = self.manager.prepare_import_data(self, model)
        params = self.manager.filter_dataset(self.settings) or {}
        action = self.manager.get('action', self.settings.data_action)
        context = self.manager.prepare_context(self.settings, path)
        context = self.manager.prepare_handlers('before', self, model, context)

        if path:
            max_rows, max_cols = self.open(path)
            self.set_dimensions(
                0, max_rows, max_cols,
                import_data=True)

        use_transaction = getattr(action, 'use_transaction', False)
        if use_transaction:
            action = transaction.atomic(action)

        for row, _model in data['items']:
            model_attrs, related_attrs = self.prepare_attrs(_model)
            model_attrs.update(**params)

            kwargs = dict(
                processor=self, path=path, fields=data['fields'],
                params=params, raw_attrs=_model,
                mfields=data['mfields'],
            )

            if use_transaction:
                sid = transaction.savepoint()

            try:
                context = action(
                    model, model_attrs, related_attrs, context, **kwargs)
            except (Error, ValueError, ValidationError,
                    AttributeError, TypeError, IndexError):
                if use_transaction:
                    transaction.savepoint_rollback(sid)

                error_message = traceback.format_exc()

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

                context.update(kwargs)
                context['error_message'] = error_message

                self.manager.prepare_handlers(
                    'error', self, model, context)

        self.manager.prepare_handlers('after', self, model, context)

        # send signal to save report
        for response in import_completed.send(
                self, date=timezone.now()):
            self.report = response[1]

        return self.report
