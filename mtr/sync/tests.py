# coding: utf-8

from __future__ import unicode_literals

import django

import os
import datetime

from collections import OrderedDict

from django.utils import six
from django.utils.translation import activate

if django.get_version() >= '1.7':
    from mtr.sync.api import manager
    from mtr.sync.api.helpers import column_value
    from mtr.sync.models import Settings
else:
    from mtr_sync.api import manager
    from mtr_sync.api.helpers import column_value
    from mtr_sync.models import Settings


class ApiTestMixin(object):
    MODEL = None
    RELATED_MODEL = None
    RELATED_MANY = None
    PROCESSOR = None
    MODEL_COUNT = 20
    CREATE_PROCESSOR_AT_SETUP = True

    def setUp(self):
        self.model = self.MODEL
        self.relatedmodel = self.RELATED_MODEL
        self.manager = manager
        self.manager.processors = OrderedDict()

        if self.CREATE_PROCESSOR_AT_SETUP:
            self.manager.register('processor', item=self.PROCESSOR)

        # TODO: refactor instance creation

        activate('de')

        self.instance = self.model.objects.create(
            name=six.text_type('test instance éprouver'),
            surname='test surname',
            gender='M', security_level=10)
        self.r_instance = self.relatedmodel.objects.create(
            office='test', address='addr')
        self.tags = [
            self.RELATED_MANY(name='test'), self.RELATED_MANY(name='test1')]

        for tag in self.tags:
            tag.save()
            self.instance.tags.add(tag)

        self.instance.office = self.r_instance
        self.instance.save()
        self.instance.populate(self.MODEL_COUNT)

        self.settings = Settings.objects.create(
            action=Settings.EXPORT,
            data_action='create',
            processor=self.PROCESSOR.__name__, worksheet='test',
            model='{}.{}'.format(
                self.model._meta.app_label, self.model.__name__).lower(),
            include_header=False,
            dataset='some_dataset' if django.get_version() >= '1.7' else '',
            filter_querystring='security_level__gte=10'
            '&surname__icontains=t&o=-3.2&gender__exact=M'
            '&fields=action_checkbox,name,surname,security_level,gender',
            language='de')

        if django.get_version() >= '1.7':
            self.queryset = self.manager.get_or_raise(
                'dataset', 'some_dataset')
            self.queryset = self.queryset(self.MODEL, self.settings)
        else:
            self.queryset = self.model.objects.all()
        self.queryset = self.queryset.filter(
            security_level__gte=10, surname__icontains='t',
            gender__exact='M').order_by('-security_level', 'surname')

        if self.CREATE_PROCESSOR_AT_SETUP:
            self.processor = self.manager.make_processor(self.settings)

            self.fields = self.settings.create_default_fields(add_label=False)


class ProcessorTestMixin(ApiTestMixin):

    def check_file_existence_and_delete(self, report):
        """Delete report file"""

        self.assertIsNone(os.remove(report.buffer_file.path))

    def check_report_success(self, delete=False):
        """Create report from settings and assert it's successful"""

        report = self.manager.export_data(self.settings)

        # report generated
        self.assertEqual(report.status, report.SUCCESS)
        self.assertEqual(report.action, report.EXPORT)
        self.assertIsInstance(report.completed_at, datetime.datetime)

        # file saved
        self.assertTrue(os.path.exists(report.buffer_file.path))
        self.assertTrue(os.path.getsize(report.buffer_file.path) > 0)

        if delete:
            self.check_file_existence_and_delete(report)

        return report

    def test_report_empty_import_errors(self):
        self.settings.start_row = 100
        self.settings.start_col = 18
        self.settings.end_col = 38
        self.settings.end_row = 350

        report = self.check_report_success()

        self.settings.start_row = 1
        self.settings.start_col = 1
        self.settings.end_col = 15
        self.settings.end_row = 99
        self.settings.action = self.settings.IMPORT
        self.settings.buffer_file = report.buffer_file

        report = self.manager.import_data(self.settings)

        self.assertEqual(report.errors.count(), self.settings.end_row)

        self.check_file_existence_and_delete(report)

    def check_sheet_values_and_delete_report(
            self, report, import_report=None, instances=None):
        if self.settings.start_row:
            start_row = self.settings.start_row - 1
        else:
            start_row = 0

        if self.settings.end_row:
            end_row = self.settings.end_row - 1
        else:
            end_row = self.queryset.count() - 1

        if self.settings.start_col:
            start_col = column_value(self.settings.start_col) - 1
        else:
            start_col = 0

        if self.settings.start_col and self.settings.end_col:
            fields_limit = self.settings.end_col - \
                column_value(self.settings.start_col) + 1
        else:
            fields_limit = len(self.fields)

        self.fields = self.fields[:fields_limit]

        if self.queryset.count() < end_row:
            end_row = self.queryset.count() + start_row - 1
            last = self.queryset.last()
        else:
            last = self.queryset.all()[end_row - start_row]

        first = self.queryset.first()
        if instances:
            first = instances[0]
            last = instances[-1]

        worksheet = self.open_report(report)
        self.check_values(
            worksheet, first, start_row, start_col)

        worksheet = self.open_report(report)
        self.check_values(
            worksheet, last, end_row, start_col)

        self.check_file_existence_and_delete(report)

        if import_report:
            self.assertEqual(import_report.status, import_report.SUCCESS)

    def open_report(self, report):
        """Open data file and return worksheet or other data source"""

        raise NotImplementedError

    def check_values(self, worksheet, instance, row, index_prepend=0):
        """Check instance values within data"""

        raise NotImplementedError

    def test_create_export_file_and_report_generation(self):
        self.check_report_success(delete=True)

    def test_export_all_dimension_settings(self):
        self.settings.start_row = 25
        self.settings.start_col = 'J'
        self.settings.end_col = 20
        self.settings.end_row = 250

        report = self.check_report_success()

        self.check_sheet_values_and_delete_report(report)

    def test_export_no_dimension_settings(self):
        report = self.check_report_success()

        self.check_sheet_values_and_delete_report(report)

    def test_import_create_data(self):
        self.settings.start_row = 1
        self.settings.start_col = 10
        self.settings.end_col = 20
        self.settings.end_row = 250

        report = self.check_report_success()

        before = self.settings.end_row - self.settings.start_row + 1
        if before > self.queryset.count():
            before = self.queryset.count()

        self.queryset.delete()
        for tag in self.tags:
            tag.delete()

        self.settings.action = self.settings.IMPORT
        self.settings.buffer_file = report.buffer_file
        self.settings.filter_querystring = ''

        import_report = self.manager.import_data(self.settings)

        self.check_sheet_values_and_delete_report(report, import_report)

        self.assertEqual(before, self.queryset.count())

    def test_import_update_data(self):
        report = self.check_report_success()

        self.queryset.update(surname_de='', name_de='')
        self.settings.data_action = 'update'
        self.settings.fields.filter(attribute='id') \
            .update(find=True, update=False)
        self.settings.buffer_file = report.buffer_file
        self.settings.filter_querystring = ''

        import_report = self.manager.import_data(self.settings)

        self.check_sheet_values_and_delete_report(report, import_report)

    def test_import_update_or_create(self):
        self.queryset = self.model.objects.all()
        self.settings.filter_querystring = ''
        self.settings.fields.filter(attribute__icontains='|_').delete()
        self.fields = self.settings.fields.all()
        self.settings.dataset = ''

        report = self.check_report_success()

        self.queryset.update(surname_de='', name_de='')
        self.queryset.filter(id__gt=10).delete()
        self.settings.fields.filter(attribute='id') \
            .update(find=True, update=False)

        self.settings.filter_querystring = ''
        self.settings.data_action = 'update_or_create'
        self.settings.buffer_file = report.buffer_file

        import_report = self.manager.import_data(self.settings)

        modified_instances = []
        for instance in self.queryset.all():
            if instance.id > 11:
                instance.id -= 11
            modified_instances.append(instance)

        self.check_sheet_values_and_delete_report(
            report, import_report, instances=modified_instances)

    def test_reading_empty_values(self):
        report = self.check_report_success()

        max_rows, max_cols = self.processor.open(report.buffer_file.path)
        self.processor.set_dimensions(
            0, 0, max_rows, max_cols, import_data=True)

        self.assertEqual(
            self.processor.end['col'], len(self.processor.read(10000)))

        self.assertEqual(
            ['', '', ''], self.processor.read(10000, [0, 23543, 434]))

    def test_import_data_without_model_and_fields(self):
        report = self.check_report_success()

        for field in self.settings.fields.all():
            field.delete()

        attrs = []

        self.manager.unregister('action', 'test_import')

        @self.manager.register('action')
        def test_import(model, model_attrs, related_attrs, context, **kwargs):
            attrs.append(model_attrs)

        self.settings.model = ''
        self.settings.filter_querystring = ''
        self.settings.data_action = 'test_import'
        self.settings.action = self.settings.IMPORT
        self.settings.buffer_file = report.buffer_file
        self.settings.populate_from_buffer_file()
        self.settings.create_default_fields()

        self.settings.fields.create(attribute='test', position='1')

        import_report = self.manager.import_data(self.settings)

        self.assertEqual(import_report.status, import_report.SUCCESS)

        self.assertNotEqual(attrs, [])
