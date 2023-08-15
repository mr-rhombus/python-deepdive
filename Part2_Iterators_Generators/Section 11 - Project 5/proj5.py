"""
Project Goal 1
--------------
Create a context manager that accepts a filename and provides a lazy iterator that can be used to iterate over the data in the file. The iterator should yield named tuples based on the header row in the CSV file.
"""

import csv
from collections import namedtuple
from itertools import islice

CARS_FPATH = 'cars.csv'
PERSONAL_FPATH = 'personal_info.csv'

class FileContextIterator:
    def __init__(self, fname):
        self._fname = fname

    def __enter__(self):
        self._file = open(self._fname, 'r')
        # Determine CSV sep, quotechar, ... dynamically
        sample = self._file.read(2000)
        dialect = csv.Sniffer().sniff(sample)
        # Parse with CSV reader
        self._file.seek(0)  # reset read head
        self._reader = csv.reader(self._file, dialect)
        # Create named tuple for each row of data
        self._headers = map(lambda x: x.lower(), next(self._reader))
        self._Row = namedtuple('Row', ' '.join(self._headers))
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._file.close()
        return False

    def __next__(self):
        if self._file.closed:
            raise StopIteration  # prevent iteration on closed files
        else:
            data = self._Row(*next(self._reader))
            return data

    def __iter__(self):
        return self


# Working code - switch PERSONAL_FPATH and CARS_FPATH to ensure operability
with FileContextIterator(PERSONAL_FPATH) as f:
    print('Solution 1')
    print('----------')
    print(list(islice(list(f), 5)), '\n')


"""
Project Goal 2
--------------
Re-implement Goal 1 but using a generator function instead.
HINT: You'll need to use the decorator from the contextlib module
"""

from contextlib import contextmanager

@contextmanager
def file_context_iterator_v2(fname):
    f = open(fname, 'r')
    try:
        # Determine CSV sep, quotechar, ... dynamically
        sample = f.read(2000)
        dialect = csv.Sniffer().sniff(sample)
        # Parse with CSV reader
        f.seek(0)  # reset read head
        reader = csv.reader(f, dialect)
        # Create named tuple for each row of data
        headers = next(reader)
        Row = namedtuple('Row', ' '.join(headers))
        data = (Row(*dat) for dat in reader)
        yield data
    finally:
        f.close()


# Working code
with file_context_iterator_v2(CARS_FPATH) as f:
    print('Solution 2')
    print('----------')
    print(list(islice(f, 5)))
