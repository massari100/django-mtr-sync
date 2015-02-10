# django-mtr-sync
Full-feature package for easy importing and exporting of data

Full description at [kickstarter page](https://www.kickstarter.com/projects/1625615835/django-opensource-improved-import-export-package)

## Features:
- Multilingual (i18n)
- Uses Celery for background tasks and for processing large volumes of data
- Creates reports about importing and exporting operations
- Model API - registers models for use  in package
- Field settings:
  - maps model fields with data fields
  - adds and removes fields (ability to skip fields on import)
  - includes drag&drop sorting fields
  - related models(fields) import-export by choosing main model
- Supports: CSV(native), XLS (using: xlwt-future, xlrd), XLSX (using: openpyxl optimized writer, reader mode, for fast processing of large volumes of data)
- Saves import templates for the processing of data from various sources and for simplicity
- Integration with standart django admin app
- Supports: Django 1.6+ Python 2.7, 3.3+

## Additional features
- Adapter API for supporting other formats
- Adding support of JSON, YAML, XML, ODS
- Data range settings (start, end cells in table), for example, if you need to import data where there is a header with logo or any other unnecessary information
- Permission control for import settings using django auth, to minimize human errors. For example, this would allow only the manager to choose the settings template for import and to upload files without configuring
- Export templates for (XLS, XLSX, ODS)
  - upload custom templates
  - set start cell of exporting data
- Filtration
  - Filter API — write own filters
  - Create filter from admin panel using embedded django template language, for example:
  - `{% if field|is_number %}{{ field/2 }}{% endif %}` (pseudo code)
  - Standard filters
    - If object exists in database and does not exist in import data, then delete it
    - If object exists in database and does not exist in import data, then set object parameter to whatever you want
    - Create object if it doesn't exist in database with current parameters from import
    - Assign object to main model field (ForeignKey, ManyToManyField), for example, category or tags separated by coma
- Template integration with django-grapelli, django-suit
- Periodic export for automatic updates
- Video tutorial how to set up package and use it
- Plugins for editors ckeditor and redactor — insert file from already exported files
