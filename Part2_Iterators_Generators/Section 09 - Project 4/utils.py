from collections import namedtuple
from datetime import datetime
import csv


def read_file(fname):
    """Lazily read a file line by line"""
    with open(fname) as f:
        next(f)  # skip header row
        reader = csv.reader(f, delimiter=",", quotechar='"')
        yield from reader


def get_headers(fname):
    """Get the header row of a CSV"""
    with open(fname) as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        return next(reader)


def clean_date(date, *, fmt="%Y-%m-%dT%H:%M:%SZ"):
    """Clean complex date strings"""
    return datetime.strptime(date, fmt)


def process_data(fname, dtypes, classname):
    """Create class instances for each row of a CSV"""
    headers = get_headers(fname)
    class_ = namedtuple(classname, " ".join(headers))
    for row in read_file(fname):
        casted = (dtype(val) for val,dtype in zip(row, dtypes))
        instance = class_(*casted)
        yield instance


def remove_dupes_from_list(lst):
    return list(dict.fromkeys(lst))


def read_from_iterators(*iterables):
    """Lazily yield the same row across all iterables passed"""
    yield from zip(*iterables)


def combine_multi(*iterators, classname, headers):
    """Combine 1+ iterators and return unique values for each row across all iterators"""
    # Create the class that will store the values
    class_ = namedtuple(classname, " ".join(headers))
    # Create an iterator that yields the same row across all iterators (i.e. CSV files)
    row_from_each = read_from_iterators(*iterators)
    for rows in row_from_each:
        # Ensure we don't pick up duplicate cols across CSVs
        fields_seen = []
        vals = []
        for row in rows:
            for attr in row._fields:
                if attr not in fields_seen:
                    fields_seen.append(attr)
                    val = getattr(row, attr)
                    vals.append(val)
        yield class_(*vals)


def combine_multi_no_stale(
    *iterators,
    classname,
    headers,
    stale_cutoff=datetime.strptime("3/1/2017", "%m/%d/%Y")
):
    iter_ = combine_multi(*iterators, classname=classname, headers=headers)
    for row in iter_:
        if row.last_updated < stale_cutoff:
            continue
        else:
            yield row


# Alternative method using filter fn
def combine_multi_no_stale_v2(*iterators, classname, headers, key=None):
    iter_ = combine_multi(*iterators, classname=classname, headers=headers)
    yield from filter(key, iter_)
