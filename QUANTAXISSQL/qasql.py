# -*- coding: utf-8 -*-


import bisect
import operator
import os
import sys
from itertools import groupby

from .common import Expression, ExpressionGroup, Filter

try:
    import cPickle as pickle
except:
    import pickle



def _in(a, b):
    return operator.contains(b, a)


def like(a, b):
    return operator.contains(a.lower(), b.lower())


class QASqlExpression(Expression):

    def __init__(self, **kwargs):
        super(QASqlExpression, self).__init__(**kwargs)
        self.operations = {'AND': 'AND', 'OR': 'OR',
                           'LIKE': like,
                           'GLOB': operator.contains,
                           "IN": _in,
                           '=': operator.eq, '!=': operator.ne, '<': operator.lt,
                           '<=': operator.le, '>': operator.gt, '>=': operator.ge}

    def apply(self, records):
        operation = self.operations[self.operator]
        records = [r for r in records if operation(r[self.key], self.value)]
        return records


class QASqlExpressionGroup(ExpressionGroup):

    def apply_filter(self, records):
        if self.is_dummy():
            return ""
        if self.expression:
            return self.expression.apply(records.values())
        else:
            # Parent of two expressions
            records1 = self.exp_group1.apply_filter(records)
            records2 = self.exp_group2.apply_filter(records)
            if self.exp_operator == Filter.operations.AND:
                ids1 = dict([(id(r), r) for r in records1])
                ids2 = dict([(id(r), r) for r in records2])
                ids = set(ids1.keys()) & set(ids2.keys())
                records = [ids1[_id] for _id in ids]
            else:
                ids = dict([(id(r), r) for r in records1])
                ids.update(dict([(id(r), r) for r in records2]))
                records = ids.values()
            return records


class QASqlFilter(Filter):

    def __init__(self, db, key):
        self.db = db
        self.key = key
        self.expression_group = QASqlExpressionGroup()
        self.expression_t = QASqlExpression

    def apply_filter(self, records):
        return self.expression_group.apply_filter(records)


class Index(object):
    """Class used for indexing a base on a field.
    The instance of Index is an attribute of the Base instance"""

    def __init__(self, db, field):
        self.db = db  # database object (instance of Base)
        self.field = field  # field name

    def __iter__(self):
        return iter(self.db.indices[self.field])

    def keys(self):
        return self.db.indices[self.field].keys()

    def __getitem__(self, key):
        """Lookup by key : return the list of records where
        field value is equal to this key, or an empty list"""
        ids = self.db.indices[self.field].get(key, [])
        return [self.db.records[_id] for _id in ids]


class _Base(object):

    def __init__(self, path, protocol=pickle.HIGHEST_PROTOCOL, save_to_file=True,
                 sqlite_compat=False):
        """protocol as defined in pickle / pickle.
        Defaults to the highest protocol available.
        For maximum compatibility use protocol = 0
        """
        self.path = path
        """The path of the database in the file system"""
        self.name = os.path.splitext(os.path.basename(path))[0]
        """The basename of the path, stripped of its extension"""
        self.protocol = protocol
        self.mode = None
        if path == ":memory:":
            save_to_file = False
        self.save_to_file = save_to_file
        self.sqlite_compat = sqlite_compat
        self.fields = []
        """The list of the fields (does not include the internal
        fields __id__ and __version__)"""
        # if base exists, get field names
        if save_to_file and self.exists():
            if protocol == 0:
                _in = open(self.path)  # don't specify binary mode !
            else:
                _in = open(self.path, 'rb')
            self.fields = pickle.load(_in)

    def exists(self):
        """
        Returns:
            - bool: if the database file exists
        """
        return os.path.isfile(self.path)

    def create(self, *fields, **kw):
        """
        Create a new base with specified field names.
        Args:
            - \*fields (str): The field names to create.
            - mode (str): the mode used when creating the database.
        - if mode = 'create' : create a new base (the default value)
        - if mode = 'open' : open the existing base, ignore the fields
        - if mode = 'override' : erase the existing base and create a
          new one with the specified fields
        Returns:
            - the database (self).
        """
        self.mode = kw.get("mode", 'create')
        if self.save_to_file and os.path.exists(self.path):
            if not os.path.isfile(self.path):
                raise IOError("%s exists and is not a file" % self.path)
            elif self.mode is 'create':
                raise IOError("Base %s already exists" % self.path)
            elif self.mode == "open":
                return self.open()
            elif self.mode == "override":
                os.remove(self.path)
            else:
                raise ValueError("Invalid value given for 'open': '%s'" % open)

        self.fields = []
        self.default_values = {}
        for field in fields:
            if type(field) is dict:
                self.fields.append(field["name"])
                self.default_values[field["name"]] = field.get("default", None)
            elif type(field) is tuple:
                self.fields.append(field[0])
                self.default_values[field[0]] = field[1]
            else:
                self.fields.append(field)
                self.default_values[field] = None

        self.records = {}
        self.next_id = 0
        self.indices = {}
        self.commit()
        return self

    def create_index(self, *fields):
        """
        Create an index on the specified field names
        An index on a field is a mapping between the values taken by the field
        and the sorted list of the ids of the records whose field is equal to
        this value
        For each indexed field, an attribute of self is created, an instance
        of the class Index (see above). Its name it the field name, with the
        prefix _ to avoid name conflicts
        Args:
            - fields (list): the fields to index
        """
        reset = False
        for f in fields:
            if f not in self.fields:
                raise NameError("%s is not a field name %s" % (f, self.fields))
            # initialize the indices
            if self.mode == "open" and f in self.indices:
                continue
            reset = True
            self.indices[f] = {}
            for _id, record in self.records.items():
                # use bisect to quickly insert the id in the list
                bisect.insort(self.indices[f].setdefault(record[f], []), _id)
            # create a new attribute of self, used to find the records
            # by this index
            setattr(self, '_' + f, Index(self, f))
        if reset:
            self.commit()

    def delete_index(self, *fields):
        """Delete the index on the specified fields"""
        for f in fields:
            if f not in self.indices:
                raise ValueError("No index on field %s" % f)
        for f in fields:
            del self.indices[f]
        self.commit()

    def open(self):
        """Open an existing database and load its content into memory"""
        # guess protocol
        if self.protocol == 0:
            _in = open(self.path)  # don't specify binary mode !
        else:
            _in = open(self.path, 'rb')
        self.fields = pickle.load(_in)
        self.next_id = pickle.load(_in)
        self.records = pickle.load(_in)
        self.indices = pickle.load(_in)
        try:
            # If loading an old database, the default values do not exist
            self.default_values = pickle.load(_in)
        except EOFError:
            self.default_values = {}
        for f in self.indices.keys():
            setattr(self, '_' + f, Index(self, f))
        _in.close()
        self.mode = "open"
        return self

    def commit(self):
        """Write the database to a file"""
        if self.save_to_file is False:
            return
        out = open(self.path, 'wb')
        pickle.dump(self.fields, out, self.protocol)
        pickle.dump(self.next_id, out, self.protocol)
        pickle.dump(self.records, out, self.protocol)
        pickle.dump(self.indices, out, self.protocol)
        pickle.dump(self.default_values, out, self.protocol)
        out.close()

    def insert(self, *args, **kw):
        """
        Insert one or more records in the database.
        Parameters can be positional or keyword arguments. If positional
        they must be in the same order as in the create() method
        If some of the fields are missing the value is set to None
        Args:
            - args (values, or a list/tuple of values): The record(s) to insert.
            - kw (dict): The field/values to insert
        Returns:
            - Returns the record identifier if inserting one item, else None.
        """
        if not self.mode:
            raise RuntimeError("Database columns have not been setup!")
        if args:
            if self.sqlite_compat and isinstance(args[0], (list, tuple)):
                for e in args[0]:
                    if type(e) is dict:
                        self.insert(**e)
                    else:
                        self.insert(*e)
                return None
            kw = dict([(f, arg) for f, arg in zip(self.fields, args)])
        # initialize all fields to the default values
        import copy
        record = copy.deepcopy(self.default_values)
        # raise exception if unknown field
        for key in kw:
            if key not in self.fields:
                raise NameError("Invalid field name : %s" % key)
        # set keys and values
        for (k, v) in kw.items():
            record[k] = v
        # add the key __id__ : record identifier
        record['__id__'] = self.next_id
        # add the key __version__ : version number
        record['__version__'] = 0
        # create an entry in the dictionary self.records, indexed by __id__
        self.records[self.next_id] = record
        # update index
        for ix in self.indices.keys():
            bisect.insort(self.indices[ix].setdefault(record[ix], []), self.next_id)
        # increment the next __id__
        self.next_id += 1
        return record['__id__']

    def delete(self, remove):
        """
        Remove a single record, or the records in an iterable
        Before starting deletion, test if all records are in the base
        and don't have twice the same __id__
        Args:
            - remove (record or list of records): The record(s) to delete.
        Returns:
            - Return the number of deleted items
        """
        if isinstance(remove, dict):
            remove = [remove]
        else:
            # convert iterable into a list (to be able to sort it)
            remove = [r for r in remove]
        if not remove:
            return 0
        _ids = [r['__id__'] for r in remove]
        _ids.sort()
        keys = set(self.records.keys())
        # check if the records are in the base
        if not set(_ids).issubset(keys):
            missing = list(set(_ids).difference(keys))
            raise IndexError('Delete aborted. Records with these ids'
                             ' not found in the base : %s' % str(missing))
        # raise exception if duplicate ids
        for i in range(len(_ids) - 1):
            if _ids[i] == _ids[i + 1]:
                raise IndexError("Delete aborted. Duplicate id : %s" % _ids[i])
        deleted = len(remove)
        while remove:
            r = remove.pop()
            _id = r['__id__']
            # remove id from indices
            for indx in self.indices.keys():
                pos = bisect.bisect(self.indices[indx][r[indx]], _id) - 1
                del self.indices[indx][r[indx]][pos]
                if not self.indices[indx][r[indx]]:
                    del self.indices[indx][r[indx]]
            # remove record from self.records
            del self.records[_id]
        return deleted

    def update(self, records, **kw):
        """
        Update one record or a list of records
        with new keys and values and update indices
        Args:
           - records (record or list of records): The record(s) to update.
        """
        # ignore unknown fields
        kw = dict([(k, v) for (k, v) in kw.items() if k in self.fields])
        if isinstance(records, dict):
            records = [records]
        # update indices
        for indx in set(self.indices.keys()) & set(kw.keys()):
            for record in records:
                if record[indx] == kw[indx]:
                    continue
                _id = record["__id__"]
                # remove id for the old value
                old_pos = bisect.bisect(self.indices[indx][record[indx]], _id) - 1
                del self.indices[indx][record[indx]][old_pos]
                if not self.indices[indx][record[indx]]:
                    del self.indices[indx][record[indx]]
                # insert new value
                bisect.insort(self.indices[indx].setdefault(kw[indx], []), _id)
        for record in records:
            # update record values
            record.update(kw)
            # increment version number
            record["__version__"] += 1

    def add_field(self, field, column_type="ignored", default=None):
        """Adds a field to the database"""
        if field in self.fields + ["__id__", "__version__"]:
            raise ValueError("Field %s already defined" % field)
        if not hasattr(self, 'records'):  # base not open yet
            self.open()
        for r in self:
            r[field] = default
        self.fields.append(field)
        self.default_values[field] = default
        self.commit()

    def drop_field(self, field):
        """Removes a field from the database"""
        if field in ["__id__", "__version__"]:
            raise ValueError("Can't delete field %s" % field)
        self.fields.remove(field)
        for r in self:
            del r[field]
        if field in self.indices:
            del self.indices[field]
        self.commit()

    def __call__(self, *args, **kw):
        """Selection by field values
        db(key=value) returns the list of records where r[key] = value
        Args:
            - args (list): A field to filter on.
            - kw (dict): pairs of field and value to filter on.
        Returns:
            - When args supplied, return a Filter object that filters on
              the specified field.
            - When kw supplied, return all the records where field values matches the
              key/values in kw.
        """
        if args and kw:
            raise SyntaxError("Can't specify positional AND keyword arguments")

        if args:
            if len(args) > 1:
                raise SyntaxError("Only one field can be specified")
            elif (type(args[0]) is QASqlExpressionGroup or type(args[0]) is QASqlFilter):
                return args[0].apply_filter(self.records)
            elif args[0] not in self.fields:
                raise ValueError("%s is not a field" % args[0])
            else:
                return QASqlFilter(self, args[0])
        if not kw:
            return self.records.values()  # db() returns all the values

        # indices and non-indices
        keys = kw.keys()
        ixs = set(keys) & set(self.indices.keys())
        no_ix = set(keys) - ixs
        if ixs:
            # fast selection on indices
            ix = ixs.pop()
            res = set(self.indices[ix].get(kw[ix], []))
            if not res:
                return []
            while ixs:
                ix = ixs.pop()
                res = res & set(self.indices[ix].get(kw[ix], []))
        else:
            # if no index, initialize result with test on first field
            field = no_ix.pop()
            res = set([r["__id__"] for r in self if r[field] == kw[field]])
        # selection on non-index fields
        for field in no_ix:
            res = res & set([_id for _id in res if self.records[_id][field] == kw[field]])
        return [self[_id] for _id in res]

    def __getitem__(self, key):
        # direct access by record id
        return self.records[key]

    def _len(self, db_filter=None):
        if db_filter is not None:
            if type(db_filter) is not QASqlExpressionGroup and type(db_filter) is not QASqlFilter:
                raise ValueError("Filter argument should be of type 'QASqlExpressionGroup'"
                                 " or 'QASqlFilter': %s" % type(db_filter))
            if db_filter.is_filtered():
                return len(db_filter.apply_filter(self.records))
        return len(self.records)

    def __len__(self):
        return self._len()

    def __delitem__(self, record_id):
        """Delete by record id"""
        self.delete(self[record_id])

    def __contains__(self, record_id):
        return record_id in self.records

    def group_by(self, column, torrents_filter):
        """Returns the records grouped by column"""
        gropus = [(k, len(list(g))) for k, g in groupby(torrents_filter,
                                                        key=lambda x: x[column])]
        result = {}
        for column, count in gropus:
            result[column] = result.get(column, 0) + count
        return [(c, result[c]) for c in result]

    def filter(self, key=None):
        return QASqlFilter(self, key)

    def get_group_count(self, group_by_field, db_filter=None):
        if db_filter is None:
            db_filter = self.filter()

        gropus = [(k, len(list(g))) for k, g in groupby(db_filter,
                                                        key=lambda x: x[group_by_field])]
        groups_dict = {}
        for group, count in gropus:
            groups_dict[group] = groups_dict.get(group, 0) + count
        return [(k, groups_dict[k]) for k in groups_dict]

    def get_unique_ids(self, id_value, db_filter=None):
        """Returns a set of unique values from column"""
        if db_filter is not None and db_filter.is_filtered():
            records = self(db_filter)
        else:
            records = self()
        return set([row[id_value] for row in records])

    def get_indices(self):
        """Returns the indices"""
        return list(self.indices)


class _BasePy2(_Base):

    def __iter__(self):
        """Iteration on the records"""
        return iter(self.records.itervalues())


class _BasePy3(_Base):

    def __iter__(self):
        """Iteration on the records"""
        return iter(self.records.values())

if sys.version_info[0] == 2:
    Base = _BasePy2
else:
    Base = _BasePy3