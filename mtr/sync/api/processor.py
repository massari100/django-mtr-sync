from __future__ import unicode_literals

import os

from django.utils.six.moves import range
from django.utils.encoding import smart_text
from django.utils import timezone
from django.db import models

from .signals import export_started, export_completed, \
    import_started, import_completed
from ..settings import LIMIT_PREVIEW, FILE_PATH


class NoIndexFound(Exception):
    pass


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
        self._chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self._types = (int,)

    def column_name(self, index):
        name = ''

        while True:
            q, r = divmod(index, 26)
            name = self._chars[r] + name

            if not q:
                return name

            index = q - 1

    def column_index(self, value):
        """Return column index for given name"""

        for index in range(0, 18279):
            name = self.column_name(index)

            if name == value:
                return index

        raise NoIndexFound

    def _convert(self, value):
        for convert in self._types:
            try:
                return convert(value)
            except ValueError:
                continue

        return value

    def column(self, value):
        """Wrapper on self.column"""

        if isinstance(value, int):
            return value

        if value.isdigit():
            return int(value)

        return self.column_index(value)

    def write(self, row, value, cells=None):
        """Independend write to cell method"""

        raise NotImplementedError

    def read(self, row, value, cells=None):
        """Independend read from cell method"""

        raise NotImplementedError

    def set_dimensions(
            self, start_row, start_col, end_row, end_col, preview=False,
            import_data=False):
        """Return start, end table dimensions"""

        start = {'row': start_row, 'col': start_col}
        end = {'row': end_row, 'col': end_col}

        if self.settings.start_row and \
                self.settings.start_row > start_row:
            start['row'] = self.settings.start_row - 1

            if not import_data:
                end['row'] += start['row']

        if self.settings.end_row and \
                self.settings.end_row < end['row']:
            end['row'] = self.settings.end_row

        limit = LIMIT_PREVIEW()
        if preview and limit < end_row:
            end_row = limit + start['row'] - 1

        if self.settings.start_col:
            start_col_index = self.column(self.settings.start_col)
            if start_col_index > start_col:
                start['col'] = start_col_index - 1

                if not import_data:
                    end['col'] += start['col']

        if self.settings.end_col:
            end_col_index = self.column(self.settings.end_col)

            if end_col_index < end['col']:
                end['col'] = end_col_index

        if self.settings.include_header and import_data:
            start['row'] += 1

        self.start, self.end = start, end
        self.cells = range(start['col'], end['col'])
        self.rows = range(start['row'], end['row'])

        return (start, end)

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
                lambda f: f.name or f.attribute,
                data['fields']))

            self.write(self.start['row'], header_data)

            self.start['row'] += 1
            self.end['row'] += 1

            self.rows = range(self.start['row'], self.end['row'])

        # write data
        data = data['items']

        for row in self.rows:
            row_data = []

            for col in self.cells:
                value = next(data)
                value = value if value else ''
                if isinstance(value, list) or isinstance(value, tuple):
                    value = ','.join(map(lambda v: smart_text(v), value))

                row_data.append(value)

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

        # TODO: transaction management
        # TODO: update if, create if, delete if

        rows = (self.read(row) for row in self.rows)
        data = self.manager.prepare_import_data(self, rows)

        for _model in data:
            main_model_attrs = {}
            related_models = {}
            # TODO: sub-fields

            for key in _model['attrs'].keys():
                if '|_fk_|' in key:
                    key_model, key_attr = key.split('|_fk_|')

                    attrs = related_models.get(key_model, {})
                    attrs[key_attr] = _model['attrs'][key]
                    related_models[key_model] = attrs
                elif '|_m_|' in key:
                    key_model, key_attr = key.split('|_m_|')

                    value = _model['attrs'][key]

                    attrs = related_models.get(key_model, {})
                    attrs[key_attr] = value
                    related_models[key_model] = attrs
                else:
                    main_model_attrs[key] = _model['attrs'][key]

            instance = model(**main_model_attrs)
            model_fields = self.manager.get_model_fields(model)

            # TODO: refactor many to many attrs

            for key in related_models.keys():
                related_field = model_fields.get(key)
                related_model = related_field.rel.to

                if isinstance(related_field, models.ForeignKey):
                    related_instance = related_model(**related_models[key])
                    related_instance.save()

                    setattr(instance, key, related_instance)
                elif isinstance(related_field, models.ManyToManyField):
                    instance_attrs = []
                    rel_values = list(related_models[key].values())
                    indexes = len(rel_values[0].split(','))

                    for index in range(indexes):
                        instance_values = {}
                        for k in related_models[key].keys():
                            value = related_models[key][k] \
                                .split(',')[index]
                            if value.isdigit():
                                value = int(value)
                            instance_values[k] = value
                    instance_attrs.append(instance_values)

                    for instance_attr in instance_attrs:
                        items = getattr(instance, key)
                        instance_attr.pop('id', None)
                        items.create(**instance_attr)

            instance.save()

        if self.settings.id:
            self.report.settings = self.settings

        # send signal to save report
        for response in import_completed.send(
                self.__class__, report=self.report,
                date=timezone.now()):
            self.report = response[1]

        return self.report
