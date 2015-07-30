from __future__ import unicode_literals


class Processor(object):

    """Base implementation of reading writing and converting
     values using field settings"""

    position = 0
    file_format = None
    file_description = None

    def __init__(self, settings=None, manager=None):
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
