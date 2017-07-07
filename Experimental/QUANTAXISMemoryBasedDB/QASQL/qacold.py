# coding:utf-8

#基于sqllite结构的,内存型列数据库

try:
    import cStringIO as io

    def to_str(val, encoding="utf-8"):  # encode a Unicode string to a Python 2 str
        return val.encode(encoding)
except ImportError:
    import io
    unicode = str  # used in tests

    def to_str(val):  # leaves a Unicode unchanged
        return val

import datetime
import re
import traceback

from .common import ExpressionGroup, Filter

# test if sqlite is installed or raise exception
try:
    from sqlite3 import dbapi2 as sqlite
    from sqlite3 import OperationalError
except ImportError:
    try:
        from pysqlite2 import dbapi2 as sqlite
        from pysqlite2._sqlite import OperationalError
    except ImportError:
        print("SQLite is not installed")
        raise

# compatibility with Python 2.3
try:
    set([])
except NameError:
    from sets import Set as set  # NOQA


# classes for CURRENT_DATE, CURRENT_TIME, CURRENT_TIMESTAMP
class CurrentDate:
    def __call__(self):
        return datetime.date.today().strftime('%Y-%M-%D')


class CurrentTime:
    def __call__(self):
        return datetime.datetime.now().strftime('%h:%m:%s')


class CurrentTimestamp:
    def __call__(self):
        return datetime.datetime.now().strftime('%Y-%M-%D %h:%m:%s')

DEFAULT_CLASSES = [CurrentDate, CurrentTime, CurrentTimestamp]

# functions to convert a value returned by a SQLite SELECT

# CURRENT_TIME format is HH:MM:SS
# CURRENT_DATE : YYYY-MM-DD
# CURRENT_TIMESTAMP : YYYY-MM-DD HH:MM:SS

c_time_fmt = re.compile('^(\d{2}):(\d{2}):(\d{2})$')
c_date_fmt = re.compile('^(\d{4})-(\d{2})-(\d{2})$')
c_tmsp_fmt = re.compile('^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')


# DATE : convert YYYY-MM-DD to datetime.date instance
def to_date(date):
    if date is None:
        return None
    mo = c_date_fmt.match(date)
    if not mo:
        raise ValueError("Bad value %s for DATE format" % date)
    year, month, day = [int(x) for x in mo.groups()]
    return datetime.date(year, month, day)


# TIME : convert HH-MM-SS to datetime.time instance
def to_time(_time):
    if _time is None:
        return None
    mo = c_time_fmt.match(_time)
    if not mo:
        raise ValueError("Bad value %s for TIME format" % _time)
    hour, minute, second = [int(x) for x in mo.groups()]
    return datetime.time(hour, minute, second)


# DATETIME or TIMESTAMP : convert %YYYY-MM-DD HH:MM:SS
# to datetime.datetime instance
def to_datetime(timestamp):
    if timestamp is None:
        return None
    if not isinstance(timestamp, unicode):
        raise ValueError("Bad value %s for TIMESTAMP format" % timestamp)
    mo = c_tmsp_fmt.match(timestamp)
    if not mo:
        raise ValueError("Bad value %s for TIMESTAMP format" % timestamp)
    return datetime.datetime(*[int(x) for x in mo.groups()])


# if default value is CURRENT_DATE etc. SQLite doesn't
# give the information, default is the value of the
# variable as a string. We have to guess...
#
def guess_default_fmt(value):
    mo = c_time_fmt.match(value)
    if mo:
        h, m, s = [int(x) for x in mo.groups()]
        if (0 <= h <= 23) and (0 <= m <= 59) and (0 <= s <= 59):
            return CurrentTime
    mo = c_date_fmt.match(value)
    if mo:
        y, m, d = [int(x) for x in mo.groups()]
        try:
            datetime.date(y, m, d)
            return CurrentDate
        except:
            pass
    mo = c_tmsp_fmt.match(value)
    if mo:
        y, mth, d, h, mn, s = [int(x) for x in mo.groups()]
        try:
            datetime.datetime(y, mth, d, h, mn, s)
            return CurrentTimestamp
        except:
            pass
    return value


class SQLiteError(Exception):
    """SQLiteError"""
    pass


class Database(dict):

    def __init__(self, filename, **kw):
        """
        To create an in-memory database provide ':memory:' as filename
        Args:
            - filename (str): The name of the database file, or ':memory:'
            - kw (dict): Arguments forwarded to sqlite3.connect
        """
        dict.__init__(self)
        self.conn = sqlite.connect(filename, **kw)
        """The SQLite connection"""
        self.cursor = self.conn.cursor()
        """The SQLite connections cursor"""
        for table_name in self._tables():
            self[table_name] = Table(table_name, self)

    def __delitem__(self, table):
        # drop table
        if isinstance(table, Table):
            table = table.name
        self.cursor.execute('DROP TABLE %s' % table)
        dict.__delitem__(self, table)

    # The instance can be used as a context manager, to make sure that it is
    # closed even if an exception is raised during operations
    def __enter__(self):
        """Enter 'with' statement"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit 'with' statement"""
        self.conn.close()
        return exc_type is None

    def _tables(self):
        """Return the list of table names in the database"""
        tables = []
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for table_info in self.cursor.fetchall():
            if table_info[0] != 'sqlite_sequence':
                tables.append(table_info[0])
        return tables

    def close(self):
        """Closes the database"""
        self.conn.close()

    def commit(self):
        """Save any changes to the database"""
        self.conn.commit()

    def create(self, table_name, *fields, **kw):
        self[table_name] = Table(table_name, self).create(*fields, **kw)
        return self[table_name]


class Table(object):

    def __init__(self, table_name, db):
        """
        Args:
           - table_name (str): The name of the SQLite table.
           - db (:class:`Database <pydblite.sqlite.Database>`): The database.
        """
        self.name = table_name
        self.db = db
        self.cursor = db.cursor
        """The SQLite connections cursor"""
        self.conv_func = {}
        self.mode = "open"
        self._get_table_info()

    def __call__(self, *args, **kw):
        """
        Selection by field values.
        db(key=value) returns the list of records where r[key] = value
        Args:
           - args (list): A field to filter on.
           - kw (dict): pairs of field and value to filter on.
        Returns:
           - When args supplied, return a :class:`Filter <pydblite.common.Filter>`
             object that filters on the specified field.
           - When kw supplied, return all the records where field values matches
             the key/values in kw.
        """
        if args and kw:
            raise SyntaxError("Can't specify positional AND keyword arguments")

        use_expression = False
        if args:
            if len(args) > 1:
                raise SyntaxError("Only one field can be specified")
            if type(args[0]) is ExpressionGroup or type(args[0]) is Filter:
                use_expression = True
            elif args[0] not in self.fields:
                raise ValueError("%s is not a field" % args[0])
            else:
                return self.filter(key=args[0])

        if use_expression:
            sql = "SELECT rowid,* FROM %s WHERE %s" % (self.name, args[0])
            self.cursor.execute(sql)
            return [self._make_record(row) for row in self.cursor.fetchall()]
        else:
            if kw:
                undef = set(kw) - set(self.fields)
                if undef:
                    raise ValueError("Fields %s not in the database" % undef)
                vals = self._make_sql_params(kw)
                sql = "SELECT rowid,* FROM %s WHERE %s" % (self.name, " AND ".join(vals))
                self.cursor.execute(sql, list(kw.values()))
            else:
                self.cursor.execute("SELECT rowid,* FROM %s" % self.name)
            records = self.cursor.fetchall()
            return [self._make_record(row) for row in records]

    def __delitem__(self, record_id):
        """Delete by record id"""
        self.delete(self[record_id])

    def __getitem__(self, record_id):
        """Direct access by record id."""
        sql = "SELECT rowid,* FROM %s WHERE rowid=%s" % (self.name, record_id)
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        if res is None:
            raise IndexError("No record at index %s" % record_id)
        else:
            return self._make_record(res)

    def __iter__(self):
        """Iteration on the records"""
        self.cursor.execute("SELECT rowid,* FROM %s" % self.name)
        results = [self._make_record(r) for r in self.cursor.fetchall()]
        return iter(results)

    def __len__(self):
        return self._len()

    def _err_msg(self, sql, args=None):
        msg = "Exception for table %s.%s\n" % (self.db, self.name)
        msg += 'SQL request %s\n' % sql
        if args:
            import pprint
            msg += 'Arguments : %s\n' % pprint.saferepr(args)
        out = io.StringIO()
        traceback.print_exc(file=out)
        msg += out.getvalue()
        return msg

    def _get_table_info(self):
        """Inspect the base to get field names."""
        self.fields = []
        self.field_info = {}
        self.cursor.execute('PRAGMA table_info (%s)' % self.name)
        for field_info in self.cursor.fetchall():
            fname = to_str(field_info[1])
            self.fields.append(fname)
            ftype = to_str(field_info[2])
            info = {'type': ftype}
            # can be null ?
            info['NOT NULL'] = field_info[3] != 0
            # default value
            default = field_info[4]
            if isinstance(default, unicode):
                default = guess_default_fmt(default)
            info['DEFAULT'] = default
            self.field_info[fname] = info
        self.fields_with_id = ['__id__'] + self.fields

    def _len(self, db_filter=None):
        """Return number of matching entries"""
        if db_filter is not None and db_filter.is_filtered():
            sql = "SELECT COUNT(*) AS count FROM %s WHERE %s" % (self.name, db_filter)
        else:
            sql = "SELECT COUNT(*) AS count FROM %s;" % self.name
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return res[0]

    def _make_record(self, row, fields=None):
        """Make a record dictionary from the result of a fetch"""
        if fields is None:
            fields = self.fields_with_id
        res = dict(zip(fields, row))
        for field_name in self.conv_func:
            res[field_name] = self.conv_func[field_name](res[field_name])
        return res

    def _make_sql_params(self, kw):
        """Make a list of strings to pass to an SQL statement
        from the dictionary kw with Python types."""
        return ['%s=?' % k for k in kw.keys()]

    def _table_exists(self):
        return self.name in self.db

    def _validate_field(self, field):
        if len(field) != 2 and len(field) != 3:
            msg = "Error in field definition %s" % field
            msg += ": should be a tuple with field_name, field_info, and optionally a default value"
            raise SQLiteError(msg)
        field_sql = '%s %s' % (field[0], field[1])
        if len(field) == 3 and field[2] is not None:
            field_sql += " DEFAULT {0}".format(field[2])
        return field_sql

    def add_field(self, name, column_type="TEXT", default=None):
        """Add a new column to the table.
        Args:
           - name (string): The name of the field
           - column_type (string): The data type of the column (Defaults to TEXT)
           - default (datatype): The default value for this field (if any)
        """
        sql = "ALTER TABLE %s ADD " % self.name
        sql += self._validate_field((name, column_type, default))
        self.cursor.execute(sql)
        self.db.commit()
        self._get_table_info()

    def commit(self):
        """Save any changes to the database"""
        self.db.commit()

    def conv(self, field_name, conv_func):
        """When a record is returned by a SELECT, ask conversion of
        specified field value with the specified function."""
        if field_name not in self.fields:
            raise NameError("Unknown field %s" % field_name)
        self.conv_func[field_name] = conv_func

    def create(self, *fields, **kw):
        """
        Create a new table.
        Args:
           - fields (list of tuples): The fields names/types to create.
             For each field, a 2-element tuple must be provided:
             - the field name
             - a string with additional information like field type +
               other information using the SQLite syntax
               eg  ('name', 'TEXT NOT NULL'), ('date', 'BLOB DEFAULT CURRENT_DATE')
           - mode (str): The mode used when creating the database.
                  mode is only used if a database file already exists.
             - if mode = 'open' : open the existing base, ignore the fields
             - if mode = 'override' : erase the existing base and create a
               new one with the specified fields
        Returns:
            - the database (self).
        """
        self.mode = mode = kw.get("mode", None)

        if self._table_exists():
            if mode == "override":
                self.cursor.execute("DROP TABLE %s" % self.name)
            elif mode == "open":
                return self.open()
            else:
                raise IOError("Base '%s' already exists" % self.name)

        sql = "CREATE TABLE %s (" % self.name
        for field in fields:
            sql += self._validate_field(field) + ','
        sql = sql[:-1] + ')'
        self.cursor.execute(sql)
        self._get_table_info()
        return self

    def create_index(self, *index_columns):
        for ic in index_columns:
            sql = "CREATE INDEX index_%s on %s (%s);" % (ic, self.name, ic)
            self.cursor.execute(sql)
        self.db.commit()

    def delete(self, removed):
        """Remove a single record, or the records in an iterable.
        Before starting deletion, test if all records are in the base
        and don't have twice the same __id__.
        Returns:
             - int: the number of deleted items
        """
        sql = "DELETE FROM %s " % self.name
        if isinstance(removed, dict):
            # remove a single record
            _id = removed['__id__']
            sql += "WHERE rowid = ?"
            args = (_id,)
            removed = [removed]
            self.cursor.execute(sql, args)
        else:
            # convert iterable into a list
            removed = [r for r in removed]
            if not removed:
                return 0
            # max number of arguments for SQLITE is 999
            for _removed in (removed[500*i:500*(i+1)] 
                for i in range((len(removed)//500)+1)):
                args = [r['__id__'] for r in _removed]
                sql = "DELETE FROM %s " % self.name
                sql += "WHERE rowid IN (%s)" % (','.join(['?'] * len(args)))
                self.cursor.execute(sql, args)
                
        self.db.commit()
        return len(removed)

    def delete_index(self, *index_columns):
        for ic in index_columns:
            sql = "DROP INDEX index_%s;" % (ic)
            self.cursor.execute(sql)
        self.db.commit()

    def drop_field(self, field):
        raise SQLiteError("Dropping fields is not supported by SQLite")

    def filter(self, key=None):
        return Filter(self, key)

    def get_group_count(self, group_by, db_filter=None):
        """Return the grouped by count of the values of a column"""
        if db_filter is not None and db_filter.is_filtered():
            sql = "SELECT %s, COUNT(*) FROM %s WHERE %s GROUP BY %s " % (group_by, self.name,
                                                                         db_filter, group_by)
        else:
            sql = "SELECT %s, COUNT(*) FROM %s GROUP BY %s;" % (group_by, self.name, group_by)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_indices(self):
        indices = []
        sql = "SELECT * FROM sqlite_master WHERE type = 'index';"
        try:
            self.cursor.execute(sql)
        except OperationalError:
            return indices

        records = self.cursor.fetchall()
        for r in records:
            indices.append(r[1][len("index_"):])
        return indices

    def get_unique_ids(self, unique_id, db_filter=None):
        """Return all the unique values of a column"""
        sql = "SELECT rowid,%s FROM %s" % (unique_id, self.name)
        if db_filter is not None and db_filter.is_filtered():
            sql += " WHERE %s" % db_filter
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        return set([row[1] for row in records])

    def info(self):
        # returns information about the table
        return [(field, self.field_info[field]) for field in self.fields]

    def insert(self, *args, **kw):
        """Insert a record in the database.
        Parameters can be positional or keyword arguments. If positional
        they must be in the same order as in the :func:`create` method.
        Returns:
            - The record identifier
        """
        if args:
            if isinstance(args[0], (list, tuple)):
                return self.insert_many(args[0])
            kw = dict([(f, arg) for f, arg in zip(self.fields, args)])

        ks = kw.keys()
        s1 = ",".join(ks)
        qm = ','.join(['?'] * len(ks))
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.name, s1, qm)
        self.cursor.execute(sql, list(kw.values()))
        return self.cursor.lastrowid

    def insert_many(self, args):
        """Insert a list or tuple of records
        Returns:
            - The last row id
        """
        sql = "INSERT INTO %s" % self.name
        sql += "(%s) VALUES (%s)"
        if isinstance(args[0], dict):
            ks = args[0].keys()
            sql = sql % (', '.join(ks), ','.join(['?' for k in ks]))
            args = [[arg[k] for k in ks] for arg in args]
        else:
            sql = sql % (', '.join(self.fields),
                         ','.join(['?' for f in self.fields]))
        try:
            self.cursor.executemany(sql, args)
        except:
            raise Exception(self._err_msg(sql, args))
        # return last row id
        return self.cursor.lastrowid

    def is_date(self, field_name):
        """Ask conversion of field to an instance of datetime.date"""
        self.conv(field_name, to_date)

    def is_datetime(self, field_name):
        """Ask conversion of field to an instance of datetime.date"""
        self.conv(field_name, to_datetime)

    def is_time(self, field_name):
        """Ask conversion of field to an instance of datetime.date"""
        self.conv(field_name, to_time)

    def open(self):
        """Open an existing database."""
        return self

    def update(self, record, **kw):
        """Update the record with new keys and values."""
        vals = self._make_sql_params(kw)
        sql = "UPDATE %s SET %s WHERE rowid=?" % (self.name,
                                                  ",".join(vals))
        self.cursor.execute(sql, list(kw.values()) + [record['__id__']])
        self.db.commit()

Base = Table  # compatibility with previous versions