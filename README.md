# django-mtr-sync

## WARNING: it's under development and has major changes around commits (no migrations before release, `tasks.py recreate command`). After release in PIP it will have stable API

## Full-feature package for easy importing and exporting of data

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/mtrgroup/django-mtr-sync/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/mtrgroup/django-mtr-sync/?branch=master) [![Code Coverage](https://scrutinizer-ci.com/g/mtrgroup/django-mtr-sync/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/mtrgroup/django-mtr-sync/?branch=master) [![Build Status](https://scrutinizer-ci.com/g/mtrgroup/django-mtr-sync/badges/build.png?b=master)](https://scrutinizer-ci.com/g/mtrgroup/django-mtr-sync/build-status/master) [![Documentation Status](https://readthedocs.org/projects/django-mtr-sync/badge/?version=latest)](https://readthedocs.org/projects/django-mtr-sync/?badge=latest)

Project updates here [http://mtr.website](http://mtr.website)

Thank you guys for funding this project at [kickstarter](https://www.kickstarter.com/projects/1625615835/django-opensource-improved-import-export-package)

## Documentation
Includes only docstrings from module [http://django-mtr-sync.rtfd.org/](http://django-mtr-sync.rtfd.org/)

## How to use
1. Install package:
   `pip install git+https://github.com/mtrgroup/django-mtr-sync.git`
2. Add `mtr.sync` to `INSTALLED_APPS` in your settings file
3. Migrate models `./manage.py migrate`
4. Configure `Celery`
5. Create settings for import or export data at `/admin/mtrsync/settings/` and run action `Sync data` to start process.

## Video demonstration
- Import action: [https://www.youtube.com/watch?v=JOgQCFB-leg](https://www.youtube.com/watch?v=JOgQCFB-leg)
- Export action: [https://www.youtube.com/watch?v=L4ti1qERSLs](https://www.youtube.com/watch?v=L4ti1qERSLs)

## Features
- Import (only creating), export data
- Processor API for supporting other formats
- Uses Celery for background tasks and for processing large volumes of data
- Creates reports about importing and exporting operations
- Auto discovering models for use in package
- Data range settings (start, end cells in table), for example, if you need to import data where there is a header with logo or any other unnecessary information
- Field settings:
  - maps model fields with data fields
  - adds and removes fields (ability to skip fields on import)
  - set start cell of exporting data
  - related models(fields, supports only ForeignKey, ManyToMany) import-export by choosing main model
- Supports: CSV(native python3, unicodecsv python2), XLS (using: xlwt-future, xlrd), XLSX (using: openpyxl optimized writer, reader mode, for fast processing of large volumes of data) and ODS(odfpy)
- Saves import, export settings for the processing of data from various sources and for simplicity
- Integration with standart django admin app
- Custom filters (querysets, data-sets)
- Value processors (convert values before import or export)
- Action handler for more flexebility (for example not create model but generate source code for it, prepare data for model)
- Supports: Django 1.6-1.8 Python 2.7, 3.3+

## Working on
- Shortcuts at admin app
- Modeltransation
- Multilingual (i18n) will be added to transifex for translating
- Documentation
- Different source input (url)
- Inline support
- Dashboard without admin
- Adding support of JSON, YAML, XML
- Permission control for import settings using django auth, to minimize human errors. For example, this would allow only the manager to choose the settings template for import and to upload files without configuring
- Export templates for (XLS, XLSX, ODS)
  - upload custom templates
- Template integration with django-grapelli, django-suit
- Periodic import, export for automatic updates
- Video tutorial how to set up package and use it
- Plugins for editors ckeditor and redactor — insert file from already exported files
